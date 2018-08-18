from django.contrib import admin

from .models import *

class TimeInfoInline(admin.TabularInline):
    model = TimeInfo

class YieldInfoInline(admin.TabularInline):
    model = YieldInfo

class NoteInline(admin.TabularInline):
    model = RecipeNote

class IngredientGroupInline(admin.TabularInline):
    model = IngredientGroup
    extra = 0

class IngredientInline(admin.TabularInline):
    fk_name = "recipe"
    model = Ingredient
    extra = 0

class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 0

class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    inlines = [TimeInfoInline, YieldInfoInline, IngredientInline, InstructionInline, NoteInline]

admin.site.register(Recipe, RecipeAdmin)
