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
    source = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "")
    last_modified = models.DateTimeField(auto_now=True)
    # Additional fiels from related tables
    # time_info
    # yield_info
    # ingredient_groups
    # instructions 
    # tags
    # notes

    def __str__(self):
        return self.name

class TimeInfo(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete= models.CASCADE, related_name= "time_info")
    unit = models.CharField(max_length=CHAR_FIELD_MAX_LEN)
    total_time = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES)
    preparation_time = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES, null= True)
    cook_time = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES, null= True)

class YieldInfo(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete= models.CASCADE, related_name= "yield_info")
    unit = models.CharField(max_length=CHAR_FIELD_MAX_LEN)
    total_yield = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES)
    serving_size = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES, null = True)

class IngredientGroup(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredient_groups")
    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN, null= True)

class Ingredient(models.Model):
    group = models.ForeignKey(IngredientGroup, on_delete=models.CASCADE, related_name= "ingredients")
    unit = models.CharField(max_length=CHAR_FIELD_MAX_LEN)
    quantity = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES)
    description = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "")
    usda_code = models.PositiveIntegerField(null= True)

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, related_name="instructions")
    instruction = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "")

class Tag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, related_name="tags")
    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "")

class Note(models.Model):
    image = models.ImageField(null=True)
    text = models.CharField(max_length=CHAR_FIELD_MAX_LEN, default= "", null=True)

    class Meta:
        abstract = True

class RecipeNote(Note):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="notes")

class IngredientNote(Note):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="notes") 

class InstructionNote(Note):
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, related_name="notes")

