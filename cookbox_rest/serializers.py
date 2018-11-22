from rest_framework import serializers

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    Note,
    RecipeNote,
    IngredientNote,
    InstructionNote,
    Tag,
)

'''
Ordering in the serializers is implicit, 
relying on the ordering of JSON arrays.
'''

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ('image', 'text',)

class RecipeNoteSerializer(NoteSerializer):
    class Meta(NoteSerializer.Meta):
        model = RecipeNote

class IngredientNoteSerializer(NoteSerializer):
    class Meta(NoteSerializer.Meta):
        model = IngredientNote

class InstructionNoteSerializer(NoteSerializer):
    class Meta(NoteSerializer.Meta):
        model = InstructionNote

class IngredientSerializer(serializers.ModelSerializer):
    notes = IngredientNoteSerializer(many= True)

    class Meta:
        model = Ingredient
        fields = ('quantity', 'unit', 'description', 'usda_code', 'notes',)

class IngredientGroupSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many= True)

    class Meta:
        model = IngredientGroup
        fields = ('name', 'ingredients',)

class InstructionSerializer(serializers.ModelSerializer):
    notes = InstructionNoteSerializer(many= True)

    class Meta:
        model = Instruction
        fields = ('instruction', 'notes',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    ingredient_groups = IngredientGroupSerializer(many= True)
    instructions = InstructionSerializer(many= True)
    tags = TagSerializer(many= True)
    notes = RecipeNoteSerializer(many= True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'unit_time', 'total_time', 'preparation_time', 'cook_time', 'unit_yield', 'serving_size', 'source', 'last_modified','ingredient_groups', 'instructions', 'notes', 'tags',)
