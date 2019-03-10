# Created by Oleksandr Sorochynskyi
# On 10/03/2019

from django.test import TestCase

from cookbox_core.models import Recipe,IngredientGroup, Ingredient

class IngredientGroupModelTest(TestCase):
    def test_recipe_foreign_key_not_null(self):
        for ingredient_group in IngredientGroup.objects.all():
            self.assertIsNotNone(ingredient_group.recipe)
