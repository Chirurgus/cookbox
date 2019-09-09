from collections import OrderedDict

from django.forms import (
    Form,
    ModelForm,
    inlineformset_factory,
    modelformset_factory,
    Textarea,
    ModelChoiceField,
    ModelMultipleChoiceField,
)

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
)

class NoteForm(ModelForm):
    class Meta:
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={}),
        }
        abstract = True

class InstructionNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = InstructionNote
        abstract = False

InstructionNoteFormset = inlineformset_factory(
    parent_model=Instruction,
    model=InstructionNoteForm.Meta.model,
    form=InstructionNoteForm
    )

class IngredientNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = IngredientNote
        abstract = False

IngredientNoteFormset = inlineformset_factory(
    parent_model=Ingredient,
    model=IngredientNoteForm.Meta.model,
    form=IngredientNoteForm
    )

class RecipeNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = RecipeNote
        abstract = False

RecipeNoteFormset = inlineformset_factory(
    parent_model=Recipe,
    model=RecipeNoteForm.Meta.model,
    form=RecipeNoteForm
    )

class IngredientForm(SuperModelFormMixin, ModelForm):
    notes = InlineFormSetField(formset_class=IngredientNoteFormset)

    class Meta:
        model = Ingredient
        fields = ['position', 'quantity', 'unit', 'description']
        widgets = {
            'description': Textarea(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

IngredientFormset = inlineformset_factory(
    parent_model=IngredientGroup,
    model=IngredientForm.Meta.model,
    form=IngredientForm
    )

class IngredientGroupForm(SuperModelFormMixin, ModelForm):
    ingredients = InlineFormSetField(formset_class= IngredientFormset)

    class Meta:
        model = IngredientGroup
        fields = ['position', 'name']
        widgets = {
            'name': Textarea(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

IngredientGroupFormset = inlineformset_factory(
    parent_model=Recipe, 
    model=IngredientGroupForm.Meta.model,
    form=IngredientGroupForm
    )

class InstructionForm(SuperModelFormMixin, ModelForm):
    notes = InlineFormSetField(formset_class= InstructionNoteFormset)

    class Meta:
        model = Instruction
        fields = ['position', 'instruction']
        widgets = {
            'instruction': Textarea(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

InstructionFormset = inlineformset_factory(
    parent_model=Recipe,
    model=InstructionForm.Meta.model,
    form=InstructionForm
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
            'name': Textarea(attrs={}),
            'description': Textarea(attrs={}),
            'source': Textarea(attrs={}),
        }