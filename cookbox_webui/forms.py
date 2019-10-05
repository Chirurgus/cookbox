# Created by Oleksandr Sorochynskyi
# On 22/09/2019

"""
Forms for the Web UI of Cookbox.

Forms in this file can be divided into 3 groups: Recipe,
Tag, and Search.
Recipe forms are all the forms of Recipes or its components 
and build up to RecipeForm which is used to create/edit
recipes. Forms for the recipe components (eg. IngredientForm)
can be used on their own in principle. Tag forms are for
creating and editing tags. Finally SearchForm is a simple form
to gather information for searching for recipes.

RecipeForm is composed of its own fields on top of formsets
for forms for recipe components. To achieve this while retaining
the same interface as the standard ModelForm two thigs were
required:
    - Superforms to include formsets as fields
    - CookboxInlineFormset allows for dynamic replication
      of nested formsets
    - ModelFormWithInlineFormsetMixin to save the nested formsets
"""
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
    '''
    Allows to change the prefix string of the empty_form via
    `self.empty_form_prefix`.

    Forms are added to formsets on the client-side by replacing
    '__prefix__' string in the empty_form html. This does not
    work for nested formsets since the empty_form will contain
    the empty_form for the nested formset. By changing the
    '__prefix__' to something else for every formset class we
    ensure that only the correct __prefix__'s are replaced.
    '''
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

class ModelFormWithInlineFormsetMixin(object):
    '''
    Allow nested forms to be automatically saved.

    If a form containing an InlineFormset is dynamically created on the
    client the forms in the formset will not have an id of their parent
    (because it doesn't have one yet). This means that we first need to save
    the parent form and only then the child form can be saved. However, by
    default, the forms first saves its children, and only then saves the
    parent. This is why this class has to be used to save children an
    additional time after the parent has been saved.

    Deleted forms should not be saved, since their instance would already be
    deleted by super().save().
    '''

    def save(self, commit=True):
        '''
        (Re)saves the related formsets, so that newly created
        nested formsets are also saved.
        '''
        # Save the parent
        ret = super().save(commit)
        if hasattr(self, 'formsets'):
            for formset in self.formsets.values():
                for form in formset.forms:
                    if not form in formset.deleted_forms:
                        form.save(commit)
        return ret
        

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

class IngredientForm(
    ModelFormWithInlineFormsetMixin,
    SuperModelFormMixin,
    ModelForm):
    notes = InlineFormSetField(formset_class=IngredientNoteFormset)

    class Meta:
        model = Ingredient
        fields = ['position', 'quantity', 'unit', 'description']

class IngredientInlineFormset(CookboxInlineFormset):
    empty_form_prefix = '__ingredient_prefix__'

IngredientFormset = inlineformset_factory(
    parent_model=IngredientGroup,
    model=IngredientForm.Meta.model,
    form=IngredientForm,
    formset=IngredientInlineFormset,
    extra=0
)

class IngredientGroupForm(
    ModelFormWithInlineFormsetMixin,
    SuperModelFormMixin,
    ModelForm):
    ingredients = InlineFormSetField(formset_class= IngredientFormset)

    class Meta:
        model = IngredientGroup
        fields = ['position', 'name']

class IngredientGroupInlineFormset(CookboxInlineFormset):
    empty_form_prefix = '__ingredient_group_prefix__'

IngredientGroupFormset = inlineformset_factory(
    parent_model=Recipe, 
    model=IngredientGroupForm.Meta.model,
    form=IngredientGroupForm,
    formset=IngredientGroupInlineFormset,
    extra=0
)

class InstructionForm(
    ModelFormWithInlineFormsetMixin,
    SuperModelFormMixin,
    ModelForm):
    notes = InlineFormSetField(formset_class= InstructionNoteFormset)

    class Meta:
        model = Instruction
        fields = ['position', 'instruction']

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

class RecipeForm(
    ModelFormWithInlineFormsetMixin,
    SuperModelFormMixin,
    ModelForm):
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
        '''
        ret = super().save(commit)
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
            "cookbox_webui/js/recipe_form.js",
            "cookbox_webui/js/html5sortable.min.js",
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
            'description': Textarea(attrs={}),
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
