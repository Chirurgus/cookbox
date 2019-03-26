# Created by Oleksandr Sorochynskyi
# On 10/03/2019

from django.test import TestCase

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
)

class IngredientGroupModelTest(TestCase):
    def setUp(self):
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

        for i in seq(10):
            Ingredient(
                group= ing_roup,
                unit= "a unit",
                quantity= i,
                description= "a test ingredient",
                position= i
            )
        
        for i in seq(10):
            Instructions(
                recipe= recipe,
                instruction= "step" + str(i),
                position= i
            )