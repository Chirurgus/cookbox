# Created by Oleksandr Sorochynskyi
# On 10/03/2019

from django.contrib.auth.models import User

from django.test import TestCase

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    IngredientNote,
    InstructionNote,
    RecipeNote,
    TagCategory,
    Tag,
)


class CookboxBaseTest(TestCase):
    """
    Base class for all cookbox TestCases.
    In setUp creates an instance of a recipe.
    """

    recipe_data = {
        "name": "Test recipe",
        "description": "A test recipe",
        "unit_time": "minutes",
        "total_time": 30,
        "preparation_time": 10,
        "cook_time": 10,
        "unit_yield": "test recipe",
        "total_yield": 1,
        "serving_size": 1,
        "source": "me",
    }

    ingredient_group_data = {
        "name": "an test ingredient group",
        "position": 0,
    }

    ingredient_data = {
        "unit": "a unit",
        "quantity": 1,
        "description": "a test ingredient",
        "position": 1,
    }

    note_data = {
        "text": "A test note",
        "image": None,
    }

    tag_data = {
        "name": "A test tag",
    }

    tag_category_data = {
        "name": "A test tag category",
    }

    user = "testuser123"
    user_pswrd = "password123"

    def setUp(self):
        user = User.objects.create(username=self.user)
        user.set_password(self.user_pswrd)
        user.save()

    def authenticate(self):
        self.client.login(username=self.user, password=self.user_pswrd)


class RecipeModelTest(CookboxBaseTest):
    def test_recipe_str(self):
        recipe_name = "New recipe name"
        recipe_data = self.recipe_data
        recipe_data.update({"name": recipe_name})

        recipe = Recipe(**recipe_data)
        self.assertEqual(recipe_name, str(recipe))


class TagModelTest(CookboxBaseTest):
    def test_tag_str(self):
        # Use only lower case tag name since
        # tag names are supposed to be lower case
        tag_name = "only miniscule tag name"

        tag = Tag(name=tag_name)
        self.assertEqual(tag_name, str(tag))

    def test_tag_save_converts_to_lower(self):
        tag_name1 = "UPPER ONLY TAG NAME"
        tag_name2 = "lower only tag name"
        tag_name3 = "mIxEd CasE tAG NAMe"

        tag1 = Tag(name=tag_name1)
        tag2 = Tag(name=tag_name2)
        tag3 = Tag(name=tag_name3)

        self.assertEqual(tag_name1, str(tag1))
        self.assertEqual(tag_name2, str(tag2))
        self.assertEqual(tag_name3, str(tag3))
