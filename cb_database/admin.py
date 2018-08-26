from django.contrib import admin

from .models import *

class TimeInfoInline(admin.TabularInline):
    model = TimeInfo

class YieldInfoInline(admin.TabularInline):
    model = YieldInfo

class RecipeNoteInline(admin.TabularInline):
    model = RecipeNote
    extra = 0

class IngredientNoteInline(admin.TabularInline):
    model = IngredientNote
    extra = 0

class InstructionNoteInline(admin.TabularInline):
    model = InstructionNote
    extra = 0

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0
    inlines = [IngredientNoteInline]

class IngredientGroupInline(admin.StackedInline):
    model = IngredientGroup
    extra = 0
    inlines = [IngredientInline]

class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 0
    inlines = [InstructionNoteInline]

class TagInline(admin.TabularInline):
    model = Tag
    extra = 0

class RecipeAdmin(admin.ModelAdmin):
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
