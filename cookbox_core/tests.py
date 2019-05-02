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

    recipe_data = {
        "name"              : "Test recipe",
        "description"       : "A test recipe",
        "unit_time"         : "minutes",
        "total_time"        : 30,
        "preparation_time"  : 10,
        "cook_time"         : 10,
        "unit_yield"        : "test recipe",
        "total_yield"       : 1,
        "serving_size"      : 1,
        "source"            : "me",
    }

    def setUp(self):
        '''
        Create an instance of a recipe and add to the (temporary) database
        '''
        recipe = Recipe(**self.recipe_data)
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

        tag = Tag(name= "a test tag", category= tag_category)
        tag.save()

class RecipeModelTest(RecipeBaseTest):
    def test_recipe_str(self):
        recipe_name = "New recipe name"
        recipe_data = self.recipe_data
        recipe_data.update({'name' : recipe_name})

        recipe = Recipe(**recipe_data)
        self.assertEquals(recipe_name, str(recipe))

class TagModelTest(RecipeBaseTest):
    def test_tag_str(self):
        # Use only lower case tag name since
        # tag names are supposed to be lower case
        tag_name = "only miniscule tag name"

        tag = Tag(name= tag_name)
        self.assertEquals(tag_name, str(tag))
    
    def test_tag_save_converts_to_lower(self):
        tag_name1 = "UPPER ONLY TAG NAME"
        tag_name2 = "lower only tag name"
        tag_name3 = "mIxEd CasE tAG NAMe"

        tag1 = Tag(name= tag_name1)
        tag2 = Tag(name= tag_name2)
        tag3 = Tag(name= tag_name3)

        self.assertEqual(tag_name1, str(tag1))
        self.assertEqual(tag_name2, str(tag2))
        self.assertEqual(tag_name3, str(tag3))