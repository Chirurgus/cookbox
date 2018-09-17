from django.forms import *
from cb_database.models import *

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['id']

class TimeInfoForm(ModelForm):
    class Meta:
        model = TimeInfo
        exclude = ['id', 'recipe']

class YieldInfoForm(ModelForm):
    class Meta:
        model = YieldInfo
        exclude = ['id', 'recipe']

class IngredientGroupForm(ModelForm):
    class Meta:
        model = IngredientGroup
        exclude = ['id']

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        exclude = ['id']

class InstructionForm(ModelForm):
    class Meta:
        model = Instruction
        exclude = ['id']

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


IngredientGroupFormset =inlineformset_factory(Recipe, IngredientGroup, form= IngredientGroupForm)
IngredientFormset = inlineformset_factory(IngredientGroup, Ingredient, form= IngredientForm)
InstructionFormset = inlineformset_factory(Recipe, Instruction, form= InstructionForm)
TagFormset = inlineformset_factory(Recipe, Tag, form= TagForm)
RecipeNoteFormset = inlineformset_factory(Recipe, RecipeNote, form= RecipeNoteForm)
IngredientNoteFormset = inlineformset_factory(Ingredient, IngredientNote, form= IngredientNoteForm)
InstructionNoteFormset = inlineformset_factory(Instruction, InstructionNote, form= InstructionNoteForm)
