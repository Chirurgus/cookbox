""" Created by Oleksandr Sorochynskyi """
""" On 03/04/2019 """

from django.test import Client
from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import User

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    Tag,
    TagCategory,
)
from cookbox_core.tests import RecipeBaseTest

class WebuiBaseTest(RecipeBaseTest):
    '''
    Authenticates the client and adds a .client member variable.
    This is done in setUp.
    Remember to call super(...).setUp() after overriding.
    '''

    user = "testuser123"
    user_pswrd = "password123"

    def setUp(self):
        super(WebuiBaseTest, self).setUp()

        user = User.objects.create(username=self.user)
        user.set_password(self.user_pswrd)
        user.save()

        self.client = Client()
        self.client.login(username=self.user,
                          password=self.user_pswrd)

class ListViewTest(WebuiBaseTest):
    def test_list_view_get_200(self):
        response = self.client.get(reverse('recipe-list'))

        self.assertEqual(response.status_code, 200)

class DetailViewTest(WebuiBaseTest):
    def test_detail_view_get_200(self):
        recipe = Recipe.objects.all().first()
        # if there are no recipes
        if recipe is None:
            self.fail(msg="There are no recipes in the set-up database")
        
        response = self.client.get(
            reverse('recipe-detail', kwargs= {'pk' : recipe.id })
            )

        self.assertEqual(response.status_code, 200)

class RecipeImport(WebuiBaseTest):
    def test_import_view_get_200(self):
        response = self.client.get(reverse('recipe-import'))

        self.assertEqual(response.status_code, 200)

class RecipeCreateViewTest(WebuiBaseTest):
    def test_create_view_get_200(self):
        response = self.client.get(reverse('recipe-create'))

        self.assertEqual(response.status_code, 200)
 
class RecipeEditViewTest(WebuiBaseTest):
    def test_edit_view_get_200(self):
        recipe = Recipe.objects.all().first()
        # if there are no recipes
        if recipe is None:
            self.fail(msg="There are no recipes in the set-up database")
        
        response = self.client.get(
            reverse('recipe-edit', kwargs= {'pk' : recipe.id })
            )

        self.assertEqual(response.status_code, 200)

class RecipeDeleteViewTest(WebuiBaseTest):
    def test_delete_view_get_200(self):
        recipe = Recipe.objects.all().first()
        # if there are no recipes
        if recipe is None:
            self.fail(msg="There are no recipes in the set-up database")
        
        response = self.client.get(
            reverse('recipe-delete', kwargs= {'pk' : recipe.id })
            )

        self.assertEqual(response.status_code, 200)

class RecipeSearchViewTest(WebuiBaseTest):
    def recipe_search_view_200(self):
        response = self.client.get(reverse('recipe-search'))

        self.assertEqual(response.status_code, 200)

class RandomRecipeViewTest(WebuiBaseTest):
    def random_recipe_view_200(self):
        response = self.client.get(reverse('recipe-random'))

        self.assertEqual(response.status_code, 200)

class RecipeSearchRandomViewTest(WebuiBaseTest):
    def recipe_search_random_view_200(self):
        response = self.client.get(reverse('recipe-search-random'))

        self.assertEqual(response.status_code, 200)

class TagListViewTest(WebuiBaseTest):
    def test_tag_list_view_200(self):
        response = self.client.get(reverse('tag-list'))

        self.assertEqual(response.status_code, 200)
       
class TagCreateViewTest(WebuiBaseTest):
    def test_tag_create_view_200(self):
        response = self.client.get(reverse('tag-create'))

        self.assertEqual(response.status_code, 200)

class TagEditViewTest(WebuiBaseTest):
    def test_tag_edit_view_200(self):
        tag = Tag.objects.all().first()
        # if there are no recipes
        if tag is None:
            self.fail(msg="There are no tags in the set-up database")
        
        response = self.client.get(
            reverse('tag-edit', kwargs= {'pk' : tag.id })
            )

        self.assertEqual(response.status_code, 200)

class TagCategoryCreateViewTest(WebuiBaseTest):
    def test_tag_category_create_view_200(self):
        response = self.client.get(reverse('tag-category-create'))

        self.assertEqual(response.status_code, 200)

class TagCategoryEditViewTest(WebuiBaseTest):
    def test_tag_category_edit_view_200(self):
        tag_category = TagCategory.objects.all().first()
        # if there are no recipes
        if tag_category is None:
            self.fail(msg="There are no tag categories in the set-up database")
        
        response = self.client.get(
            reverse('tag-category-edit', kwargs= {'pk' : tag_category.id })
            )

        self.assertEqual(response.status_code, 200)

class TagCategoryDeleteViewTest(WebuiBaseTest):
    def test_tag_category_delete_view_200(self):
        tag_category = TagCategory.objects.all().first()
        # if there are no recipes
        if tag_category is None:
            self.fail(msg="There are no tag categories in the set-up database")
        
        response = self.client.get(
            reverse('tag-category-delete', kwargs= {'pk' : tag_category.id })
            )

        self.assertEqual(response.status_code, 200)
