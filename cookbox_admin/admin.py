from django.contrib import admin
import nested_admin

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

class RecipeNoteInline(nested_admin.NestedTabularInline):
    model = RecipeNote
    extra = 0

class IngredientNoteInline(nested_admin.NestedTabularInline):
    model = IngredientNote
    extra = 0

class InstructionNoteInline(nested_admin.NestedTabularInline):
    model = InstructionNote
    extra = 0

class IngredientInline(nested_admin.NestedTabularInline):
    model = Ingredient
    extra = 0
    sortable_field_name = "position"
    inlines = [IngredientNoteInline]

class IngredientGroupInline(nested_admin.NestedStackedInline):
    model = IngredientGroup
    extra = 0
    sortable_field_name = "position"
    inlines = [IngredientInline]

class InstructionInline(nested_admin.NestedTabularInline):
    model = Instruction
    extra = 0
    sortable_field_name = "position"
    inlines = [InstructionNoteInline]

class RecipeAdmin(nested_admin.NestedModelAdmin):
    model = Recipe
    inlines = [
        IngredientGroupInline,
        InstructionInline,
        RecipeNoteInline,
    ]

class TagAdmin(nested_admin.NestedModelAdmin):
    model = Tag


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
