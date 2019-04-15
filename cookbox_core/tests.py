# Created by Oleksandr Sorochynskyi
# On 10/03/2019

from django.test import TestCase

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    TagCategory,
    Tag,
)

class RecipeBaseTest(TestCase):
    '''
    Base class for all cookbox TestCases.
    In setUp creates an instance of a recipe.
    '''
    def setUp(self):
        '''
        Create an instance of a recipe and add to the (temporary) database
        '''
        recipe = Recipe(name="Test recipe",
               description= "A test recipe",
               unit_time= "minutes",
               total_time= 30,
               preparation_time= 10,
               cook_time= 10,
               unit_yield= "test recipe",
               total_yield= 1,
               serving_size= 1,
               source= "me"
        )
        recipe.save()

        ing_group = IngredientGroup(
            recipe= recipe,
            name= "an test ingredient group",
            position= 0
        )

        for i in range(10):
            Ingredient(
                group= ing_group,
                unit= "a unit",
                quantity= i,
                description= "a test ingredient",
                position= i
            )
        
        for i in range(10):
            Instruction(
                recipe= recipe,
                instruction= "step" + str(i),
                position= i
            )
        
        tag_category = TagCategory(name="Test tag category")
        tag_category.save()

        tag = TagCategory(name= "a test tag",
                          category= tag_category 
                          )
        tag.save()

class IngredientGroupModelTest(RecipeBaseTest):
    pass