from .models import *
from rest_framework import serializers

class RecipeNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeNote
        exclude = ('id','recipe',)

class IngredientNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientNote
        exclude = ('id','ingredient',)

class InstructionNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructionNote
        exclude = ('id','instruction',)

class TimeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeInfo
        exclude = ('id', 'recipe',)

class YieldInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldInfo
        exclude = ('id', 'recipe',)

class IngredientSerializer(serializers.ModelSerializer):
    notes = IngredientNoteSerializer(many= True)

    class Meta:
        model = Ingredient
        exclude = ('id',)

class IngredientGroupSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many= True)

    class Meta:
        model = IngredientGroup
        exclude = ('recipe',)

class InstructionSerializer(serializers.ModelSerializer):
    notes = InstructionNoteSerializer(many= True)

    class Meta:
        model = Instruction
        exclude = ('id', 'recipe',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('id', 'recipe',)


class RecipeSerializer(serializers.ModelSerializer):
    time_info = TimeInfoSerializer(many= False)
    yield_info = YieldInfoSerializer(many= False)
    ingredient_groups = IngredientGroupSerializer(many= True)
    instructions = InstructionSerializer(many= True)
    tags = TagSerializer(many= True)
    notes = RecipeNoteSerializer(many= True)

    class Meta:
        model = Recipe
        fields = '__all__'
