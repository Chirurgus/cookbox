from django.forms import *
from cb_database.models import *

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['id']

class IngredientGroupForm(ModelForm):
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


IngredientGroupFormset =inlineformset_factory(Recipe, IngredientGroup, form= IngredientGroupForm, extra= 0)
IngredientFormset = inlineformset_factory(IngredientGroup, Ingredient, form= IngredientForm, extra=0)
InstructionFormset = inlineformset_factory(Recipe, Instruction, form= InstructionForm, extra=0)
TagFormset = inlineformset_factory(Recipe, Tag, form= TagForm, extra= 0)
RecipeNoteFormset = inlineformset_factory(Recipe, RecipeNote, form= RecipeNoteForm, extra= 0)
IngredientNoteFormset = inlineformset_factory(Ingredient, IngredientNote, form= IngredientNoteForm, extra= 0)
InstructionNoteFormset = inlineformset_factory(Instruction, InstructionNote, form= InstructionNoteForm, extra= 0)
