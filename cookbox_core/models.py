# Created by Oleksandr Sorochynskyi
# On 13 08 18

from django.db import models

# Max length for CharField models
CHAR_FIELD_MAX_LEN = 256
DECIMAL_FIELD_MAX_DIGITS = 12
DECIMAL_FIELD_DPLACES = 2

class Recipe(models.Model):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "")
    description = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "")
    unit_time = models.CharField(max_length=CHAR_FIELD_MAX_LEN)
    total_time = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES)
    preparation_time = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES, null= True, blank= True)
    cook_time = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES, null= True, blank= True)
    unit_yield = models.CharField(max_length=CHAR_FIELD_MAX_LEN)
    total_yield = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES)
    serving_size = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES, null = True, blank= True)
    source = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "", blank= True)
    last_modified = models.DateTimeField(auto_now=True)
    # Additional fields from related tables
    # ingredient_groups
    # instructions 
    # tags
    # notes

    def __str__(self):
        return self.name

class IngredientGroup(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredient_groups")
    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN, null= True, blank= True)
    position = models.PositiveSmallIntegerField(null= True)

    class Meta:
        ordering = ['position']

class Ingredient(models.Model):
    group = models.ForeignKey(IngredientGroup, on_delete=models.CASCADE, related_name= "ingredients")
    unit = models.CharField(max_length=CHAR_FIELD_MAX_LEN)
    quantity = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES)
    description = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "")
    usda_code = models.PositiveIntegerField(null= True, blank= True)
    position = models.PositiveSmallIntegerField(null= True)

    class Meta:
        ordering = ['position']

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="instructions")
    instruction = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "")
    position = models.PositiveSmallIntegerField(null=True)

    class Meta:
        ordering = ['position']

class Tag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "")

class Note(models.Model):
    image = models.ImageField(null=True, blank= True)
    text = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "", null=True, blank= True)

    class Meta:
        abstract = True

class RecipeNote(Note):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="notes")

class IngredientNote(Note):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="notes") 

class InstructionNote(Note):
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, related_name="notes")
