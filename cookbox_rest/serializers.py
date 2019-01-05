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

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


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
        fields = ('quantity', 'unit', 'description', 'notes',)

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


class RecipeSerializer(DynamicFieldsModelSerializer):
    ingredient_groups = IngredientGroupSerializer(many= True)
    instructions = InstructionSerializer(many= True)
    tags = TagSerializer(many= True)
    notes = RecipeNoteSerializer(many= True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'unit_time', 'total_time', 'preparation_time', 'cook_time', 'unit_yield', 'serving_size', 'source', 'last_modified','ingredient_groups', 'instructions', 'notes', 'tags',)
