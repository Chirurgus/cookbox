""" Created by Oleksandr Sorochynskyi """
""" On 03/04/2019 """

from django.test import TestCase, Client
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
    def list_view_get_200(self):
        response = self.client.get(reverse('recipe-list'))

        self.assertEqual(response.status_code, 200)

class DetailViewTest(WebuiBaseTest):
    def detail_view_get_200(self):
        recipe = Recipe.objects.all().first()
        # if there are no recipes
        if recipe is None:
            self.fail(msg="There are no recipes in the set-up database")
        
        response = self.client.get(
            reverse('recipe-detail', {'id' : recipe.id })
            )

        self.assertEqual(response.status_code, 200)

class RecipeImport(WebuiBaseTest):
    def import_view_get_200(self):
        response = self.client.get(reverse('recipe-import'))

        self.assertEqual(response.status_code, 200)

class CreateViewTest(WebuiBaseTest):
    def create_view_get_200(self):
        response = self.client.get(reverse('recipe-create'))

        self.assertEqual(response.status_code, 200)
 
class RecipeEditViewTest(WebuiBaseTest):
    def edit_view_get_200(self):
        recipe = Recipe.objects.all().first()
        # if there are no recipes
        if recipe is None:
            self.fail(msg="There are no recipes in the set-up database")
        
        response = self.client.get(
            reverse('recipe-edit', {'id' : recipe.id })
            )

        self.assertEqual(response.status_code, 200)

class RecipeDeleteViewTest(WebuiBaseTest):
    def delete_view_get_200(self):
        recipe = Recipe.objects.all().first()
        # if there are no recipes
        if recipe is None:
            self.fail(msg="There are no recipes in the set-up database")
        
        response = self.client.get(
            reverse('recipe-delete', {'id' : recipe.id })
            )

        self.assertEqual(response.status_code, 200)

class TagListViewTest(WebuiBaseTest):
    def tag_list_view_200(self):
        response = self.client.get(reverse('tag-list'))

        self.assertEqual(response.status_code, 200)
       
class TagCreateViewTest(WebuiBaseTest):
    def tag_create_view_200(self):
        response = self.client.get(reverse('tag-create'))

        self.assertEqual(response.status_code, 200)

class TagEditViewTest(WebuiBaseTest):
    def tag_edit_view_200(self):
        tag = Tag.objects.all().first()
        # if there are no recipes
        if tag is None:
            self.fail(msg="There are no tags in the set-up database")
        
        response = self.client.get(
            reverse('tag-edit', {'id' : tag.id })
            )

        self.assertEqual(response.status_code, 200)

class TagCategoryCreateViewTest(WebuiBaseTest):
    def tag_category_create_view_200(self):
        response = self.client.get(reverse('tag-category-create'))

        self.assertEqual(response.status_code, 200)

class TagCategoryEditViewTest(WebuiBaseTest):
    def tag_category_edit_view_200(self):
        tag_category = TagCategory.objects.all().first()
        # if there are no recipes
        if tag_category is None:
            self.fail(msg="There are no tag categories in the set-up database")
        
        response = self.client.get(
            reverse('tag-category-edit', {'id' : tag_category.id })
            )

        self.assertEqual(response.status_code, 200)

class TagCategoryDeleteViewTest(WebuiBaseTest):
    def tag_category_delete_view_200(self):
        tag_category = TagCategory.objects.all().first()
        # if there are no recipes
        if tag_category is None:
            self.fail(msg="There are no tag categories in the set-up database")
        
        response = self.client.get(
            reverse('tag-category-delete', {'id' : tag_category.id })
            )

        self.assertEqual(response.status_code, 200)
