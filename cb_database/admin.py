from django.contrib import admin
import nested_admin

from .models import *

class TimeInfoInline(nested_admin.NestedTabularInline):
    model = TimeInfo

class YieldInfoInline(nested_admin.NestedTabularInline):
    model = YieldInfo

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

class TagInline(nested_admin.NestedTabularInline):
    model = Tag
    extra = 0

class RecipeAdmin(nested_admin.NestedModelAdmin):
    model = Recipe
    inlines = [
        TimeInfoInline,
        YieldInfoInline,
        IngredientGroupInline,
        InstructionInline,
        RecipeNoteInline,
        TagInline
        ]

admin.site.register(Recipe, RecipeAdmin)
