from collections import OrderedDict

from django.forms import ModelForm, inlineformset_factory, Textarea

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    RecipeNote,
    IngredientNote,
    InstructionNote,
    Tag
)

from .nested_form import BaseNestedModelForm, BaseNestedInnerFormSet, nestedformset_factory

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'unit_time', 'total_time', 'preparation_time', 'cook_time', 'unit_yield', 'total_yield', 'serving_size', 'source']
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
    

class IngredientGroupForm(BaseNestedModelForm):
    class Meta:
        model = IngredientGroup
        fields = ['position', 'name']
        widgets = {
            'name': Textarea(attrs={}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['position', 'quantity', 'unit', 'description']
        widgets = {
            'description': Textarea(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

class InstructionForm(ModelForm):
    class Meta:
        model = Instruction
        fields = ['position', 'instruction']
        widgets = {
            'instruction': Textarea(attrs={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update(tabindex=-1)

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

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

class IngredientNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = IngredientNote
        abstract = False

class RecipeNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = RecipeNote
        abstract = False


InstructionFormset = inlineformset_factory(Recipe, Instruction, form= InstructionForm, extra=0)
IngredientFormset = inlineformset_factory(IngredientGroup, Ingredient, form= IngredientForm, formset= BaseNestedInnerFormSet, extra=0)
TagFormset = inlineformset_factory(Recipe, Tag, form= TagForm, extra= 0)
RecipeNoteFormset = inlineformset_factory(Recipe, RecipeNote, form= RecipeNoteForm, extra= 0)
IngredientNoteFormset = inlineformset_factory(Ingredient, IngredientNote, form= IngredientNoteForm, extra= 0)
InstructionNoteFormset = inlineformset_factory(Instruction, InstructionNote, form= InstructionNoteForm, extra= 0)
IngredientGroupFormset = nestedformset_factory(Recipe, IngredientGroup, IngredientFormset, form= IngredientGroupForm, extra= 0)

class RecipeCompleteForm():
    RECIPE_FORM = 'recipe_form'
    INGREDIENT_GROUPS = 'ingredient_group_forms'
    INSTRUCTIONS = 'instruction_forms'
    NOTES = 'note_forms'
    TAGS = 'tag_forms'

    def __init__(self, data=None, instance=None, *args, **kwargs):
        self.forms = OrderedDict()
        self.forms[self.RECIPE_FORM] = RecipeForm(data= data, instance= instance)
        self.forms[self.INGREDIENT_GROUPS] = IngredientGroupFormset(data= data, instance= instance, prefix= 'ingredient_groups')
        self.forms[self.INSTRUCTIONS] = InstructionFormset(data= data, instance= instance, prefix= 'instructions')
        self.forms[self.NOTES] = RecipeNoteFormset(data= data, instance= instance, prefix= 'notes')
        self.forms[self.TAGS] = TagFormset(data= data, instance= instance, prefix= 'tags')

        # Create a human readable label
        self.forms[self.RECIPE_FORM].custom_label = ""
        self.forms[self.INGREDIENT_GROUPS].custom_label = "Ingredient groups"
        self.forms[self.INSTRUCTIONS].custom_label = "Instructions"
        self.forms[self.NOTES].custom_label = "Notes"
        self.forms[self.TAGS].custom_label = "Tags"

    # Inserts a new recipe instance in the database
    def create(self):
        recipe = self.forms[self.RECIPE_FORM].save()
        for key,form in self.forms.items():
            form.instance = recipe
            form.save()

    # Updates an existing recipe instance
    def save(self):
        for key,form in self.forms.items():
            form.save()

    # Checks validity of the data in the form
    def is_valid(self):
        valid = True
        recipe = self.forms[self.RECIPE_FORM].save(commit= False)
        for key, form in self.forms.items():
            if not form.instance:
                form.instance = recipe
            valid = form.is_valid() and valid 
        return valid
