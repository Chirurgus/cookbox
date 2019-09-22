from collections import OrderedDict

from django.forms import (
    Form,
    ModelForm,
    inlineformset_factory,
    modelformset_factory,
    Textarea,
    CharField,
    FloatField,
    ModelChoiceField,
    ModelMultipleChoiceField,
    BaseInlineFormSet,
)
from django.forms.widgets import CheckboxSelectMultiple

from django_superform.forms import SuperModelFormMixin
from django_superform import InlineFormSetField

from dal.autocomplete import ModelSelect2Multiple

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    RecipeNote,
    IngredientNote,
    InstructionNote,
    Tag,
    TagCategory,
    CHAR_FIELD_MAX_LEN_SHORT
)

class CookboxInlineFormset(BaseInlineFormSet):
    empty_form_prefix = '__prefix__'

    # Just copies the definition form BaseInlineFormSet
    # but replaces the hard-coded '__prefix__' by a variable
    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix(self.empty_form_prefix),
            empty_permitted=True,
            use_required_attribute=False,
            **self.get_form_kwargs(None)
        )
        self.add_fields(form, None)
        return form

class NoteForm(ModelForm):
    class Meta:
        fields = ['text']
        '''
        widgets = {
            'text': Textarea(attrs={}),
        }
        '''
        abstract = True

class NoteInlineFormset(CookboxInlineFormset):
    empty_form_prefix = '__note_prefix__'

class InstructionNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = InstructionNote
        abstract = False
    
InstructionNoteFormset = inlineformset_factory(
    parent_model=Instruction,
    model=InstructionNoteForm.Meta.model,
    form=InstructionNoteForm,
    formset=NoteInlineFormset,
    extra=0
)

class IngredientNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = IngredientNote
        abstract = False

IngredientNoteFormset = inlineformset_factory(
    parent_model=Ingredient,
    model=IngredientNoteForm.Meta.model,
    form=IngredientNoteForm,
    formset=NoteInlineFormset,
    extra=0
)

class RecipeNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = RecipeNote
        abstract = False

RecipeNoteFormset = inlineformset_factory(
    parent_model=Recipe,
    model=RecipeNoteForm.Meta.model,
    form=RecipeNoteForm,
    formset=NoteInlineFormset,
    extra=0
)

class IngredientForm(SuperModelFormMixin, ModelForm):
    notes = InlineFormSetField(formset_class=IngredientNoteFormset)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

    class Meta:
        model = Ingredient
        fields = ['position', 'quantity', 'unit', 'description']
        '''
        widgets = {
            'description': Textarea(attrs={}),
        }
        '''

class IngredientInlineFormset(CookboxInlineFormset):
    empty_form_prefix = '__ingredient_prefix__'

IngredientFormset = inlineformset_factory(
    parent_model=IngredientGroup,
    model=IngredientForm.Meta.model,
    form=IngredientForm,
    formset=IngredientInlineFormset,
    extra=0
)

class IngredientGroupForm(SuperModelFormMixin, ModelForm):
    ingredients = InlineFormSetField(formset_class= IngredientFormset)

    class Meta:
        model = IngredientGroup
        fields = ['position', 'name']
        '''
        widgets = {
            'name': Textarea(attrs={}),
        }
        '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

class IngredientGroupInlineFormset(CookboxInlineFormset):
    empty_form_prefix = '__ingredient_group_prefix__'

IngredientGroupFormset = inlineformset_factory(
    parent_model=Recipe, 
    model=IngredientGroupForm.Meta.model,
    form=IngredientGroupForm,
    formset=IngredientGroupInlineFormset,
    extra=0
)

class InstructionForm(SuperModelFormMixin, ModelForm):
    notes = InlineFormSetField(formset_class= InstructionNoteFormset)

    class Meta:
        model = Instruction
        fields = ['position', 'instruction']
        '''
        widgets = {
            'instruction': Textarea(attrs={}),
        }
        '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

class InstructionInlineFormset(CookboxInlineFormset):
    empty_form_prefix = '__instruction_prefix__'

InstructionFormset = inlineformset_factory(
    parent_model=Recipe,
    model=InstructionForm.Meta.model,
    form=InstructionForm,
    formset=InstructionInlineFormset,
    extra=0
)

class TagForm(ModelForm):
    category = ModelChoiceField(queryset= TagCategory.objects.all(),
                                required= False)

    class Meta:
        model = Tag
        fields = ['name', 'category']

class TagCategoryForm(ModelForm):
    class Meta:
        model = TagCategory
        fields = ['name']

class RecipeForm(SuperModelFormMixin, ModelForm):
    ingredient_groups = InlineFormSetField(formset_class= IngredientGroupFormset)
    instructions = InlineFormSetField(formset_class= InstructionFormset)
    notes = InlineFormSetField(formset_class= RecipeNoteFormset)
    tags = ModelMultipleChoiceField(queryset= Tag.objects.all(),
                                    widget= ModelSelect2Multiple(url= 'recipe-tag-autocomplete'),
                                    required= False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        recipe = kwargs.get('instance')
        if not recipe is None:
            self.fields['tags'].initial = recipe.tags.all()
        else:
            self.fields['tags'].inital = []

    def save(self, commit=True):
        '''
        Same as ModelForm.save(), but also saves tags if commit=True
        Also (re)saves the related formsets, so that newly created
        nested formsets are also created.
        '''
        ret = super().save(commit)
        for formset in self.formsets.values():
            for form in formset.forms:
                form.save(commit)
                if hasattr(form, 'formsets'):
                    for nested_formset in form.formsets.values():
                        for nested_form in nested_formset.forms:
                            nested_form.save(commit)
        if commit:
            self.save_tags()
        return ret
    
    def save_tags(self):
        '''
        Saves tags many2many field.
        Gets called automatically from save(commit=True) method.
        '''
        self.instance.tags.set(self.cleaned_data['tags'])
    
    class Media:
        css = {
            'all' : (
                'cookbox_webui/css/recipe_form.css',
            )
        }
        js = (
            'cookbox_webui/js/recipe_form.js',
        )
        
    class Meta:
        model = Recipe
        fields = [
            'name',
            'description',
            'unit_time',
            'total_time',
            'preparation_time',
            'cook_time',
            'unit_yield',
            'total_yield',
            'serving_size',
            'source',
            'image',
            'tags',
        ]
        labels = {
            'name': 'Recipe name',
            'unit_time': 'Time measurement unit',
            'unit_yield': 'Yield measurement unit',
        }
        widgets = {
            #'name': Textarea(attrs={}),
            'description': Textarea(attrs={}),
            #'source': Textarea(attrs={}),
        }

class SearchForm(Form):
    name = CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, required=False)
    source = CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, required=False)
    max_duration = FloatField(required=False)
    min_duration = FloatField(required=False)
    tags = ModelMultipleChoiceField(
        required=False,
        to_field_name= 'name',
        queryset= Tag.objects.all(),
        widget= CheckboxSelectMultiple()
    )
