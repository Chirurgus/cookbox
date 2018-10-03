from django.forms import *
from cb_database.nested_form import BaseNestedModelForm, BaseNestedInnerFormSet, nestedformset_factory
from cb_database.models import *

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['id']

class IngredientGroupForm(BaseNestedModelForm):
    class Meta:
        model = IngredientGroup
        exclude = ['id','position']

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        exclude = ['id','position']

class InstructionForm(ModelForm):
    class Meta:
        model = Instruction
        exclude = ['id', 'position']

class TagForm(ModelForm):
    class Meta:
        model = Tag
        exclude = ['id']

class InstructionNoteForm(ModelForm):
    class Meta:
        model = InstructionNote
        exclude = ['id']

class IngredientNoteForm(ModelForm):
    class Meta:
        model = IngredientNote
        exclude = ['id']

class RecipeNoteForm(ModelForm):
    class Meta:
        model = RecipeNote
        exclude = ['id']


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
        self.forms = {self.RECIPE_FORM : RecipeForm(data= data, instance= instance),
                      self.INGREDIENT_GROUPS : IngredientGroupFormset(data= data, instance= instance, prefix= 'ingredient_groups'),
                      self.INSTRUCTIONS : InstructionFormset(data= data, instance= instance, prefix= 'instructions'),
                      self.NOTES : RecipeNoteFormset(data= data, instance= instance, prefix= 'notes'),
                      self.TAGS : TagFormset(data= data, instance= instance, prefix= 'tags') }

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
