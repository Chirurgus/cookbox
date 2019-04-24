# Created by Oleksandr Sorochynskyi
# On 13 08 18

from django.db import models

# Max length for CharField models
CHAR_FIELD_MAX_LEN_SHORT = 126
CHAR_FIELD_MAX_LEN_MEDIUM = 256
CHAR_FIELD_MAX_LEN_LONG = 1024
DECIMAL_FIELD_MAX_DIGITS = 12
DECIMAL_FIELD_DPLACES = 2

class Recipe(models.Model):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM, default= "")
    description = models.CharField(max_length=CHAR_FIELD_MAX_LEN_LONG, default= "")
    unit_time = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM)
    total_time = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES)
    preparation_time = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES, null= True, blank= True)
    cook_time = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES, null= True, blank= True)
    unit_yield = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM)
    total_yield = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES)
    serving_size = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES, null = True, blank= True)
    source = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM, default= "", blank= True)
    image = models.ImageField(null=True, blank= True)
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
    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM, null= True, blank= True)
    position = models.PositiveSmallIntegerField(null= True)

    class Meta:
        ordering = ['position']

class Ingredient(models.Model):
    group = models.ForeignKey(IngredientGroup, on_delete=models.CASCADE, related_name= "ingredients")
    unit = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM, blank=True)
    quantity = models.DecimalField(max_digits=DECIMAL_FIELD_MAX_DIGITS,decimal_places=DECIMAL_FIELD_DPLACES)
    description = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM, default= "")
    position = models.PositiveSmallIntegerField(null= True)

    class Meta:
        ordering = ['position']

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="instructions")
    instruction = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM, default= "")
    position = models.PositiveSmallIntegerField(null=True)

    class Meta:
        ordering = ['position']

class TagCategory(models.Model):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, unique= True, null= False, blank= False)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, unique= True, null= False, blank= False)
    category = models.ForeignKey(TagCategory, on_delete=models.CASCADE, related_name="tags", null=True)
    recipes = models.ManyToManyField(Recipe, related_name="tags")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Tag, self).save(*args, **kwargs)

class Note(models.Model):
    image = models.ImageField(null=True, blank= True)
    text = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM, default= "", null=True, blank= True)

    class Meta:
        abstract = True

class RecipeNote(Note):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="notes")

class IngredientNote(Note):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="notes") 

class InstructionNote(Note):
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, related_name="notes")
