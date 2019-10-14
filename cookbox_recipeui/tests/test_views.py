# Created by Oleksandr Sorochynskyi
# On 13/10/2019

from django.urls import reverse,reverse_lazy

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    Tag,
    TagCategory,
)

from cookbox_core.tests import CookboxBaseTest

class ListViewTest(CookboxBaseTest):
    def test_requires_auth(self):
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, 302)

    def test_list_view_get_200(self):
        self.authenticate()
        response = self.client.get(reverse('recipe-list'))
        self.assertEqual(response.status_code, 200)

class DetailViewTest(CookboxBaseTest):
    def test_requires_auth(self):
        recipe = Recipe(**self.recipe_data)
        recipe.save()
        response = self.client.get(
            reverse('recipe-detail', kwargs= {'pk' : recipe.id })
        )
        self.assertEqual(response.status_code, 302)

    def test_detail_view_get_200(self):
        self.authenticate()
        recipe = Recipe(**self.recipe_data)
        recipe.save()
        response = self.client.get(
            reverse('recipe-detail', kwargs= {'pk' : recipe.id })
        )
        self.assertEqual(response.status_code, 200)

class RecipeImport(CookboxBaseTest):
    def test_requires_auth(self):
        response = self.client.get(reverse('recipe-import'))
        self.assertEqual(response.status_code, 302)

    def test_import_view_get_200(self):
        self.authenticate()
        response = self.client.get(reverse('recipe-import'))
        self.assertEqual(response.status_code, 200)

class RecipeCreateViewTest(CookboxBaseTest):
    def test_requires_auth(self):
        response = self.client.get(reverse('recipe-create'))
        self.assertEqual(response.status_code, 302)

    def test_create_view_get_200(self):
        self.authenticate()
        response = self.client.get(reverse('recipe-create'))
        self.assertEqual(response.status_code, 200)
 
class RecipeEditViewTest(CookboxBaseTest):
    def test_requires_auth(self):
        recipe = Recipe(**self.recipe_data)
        recipe.save()
        response = self.client.get(
            reverse('recipe-edit', kwargs= {'pk' : recipe.id })
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_view_get_200(self):
        self.authenticate()
        recipe = Recipe(**self.recipe_data)
        recipe.save()
        response = self.client.get(
            reverse('recipe-edit', kwargs= {'pk' : recipe.id })
        )
        self.assertEqual(response.status_code, 200)

class RecipeDeleteViewTest(CookboxBaseTest):
    def test_requires_auth(self):
        recipe = Recipe(**self.recipe_data)
        recipe.save()
        response = self.client.get(
            reverse('recipe-delete', kwargs= {'pk' : recipe.id })
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_view_get_200(self):
        self.authenticate()
        recipe = Recipe(**self.recipe_data)
        recipe.save()
        response = self.client.get(
            reverse('recipe-delete', kwargs= {'pk' : recipe.id })
        )
        self.assertEqual(response.status_code, 200)

class RecipeSearchViewTest(CookboxBaseTest):
    def test_requires_auth(self):
        response = self.client.get(reverse('recipe-search'))
        self.assertEqual(response.status_code, 302)

    def test_recipe_search_view_200(self):
        self.authenticate()
        response = self.client.get(reverse('recipe-search'))
        self.assertEqual(response.status_code, 200)

class RandomRecipeViewTest(CookboxBaseTest):
    def test_requires_auth(self):
        Recipe(**self.recipe_data).save()
        response = self.client.get(reverse('recipe-random'))
        self.assertEqual(response.status_code, 302)

    def test_random_recipe_view_200_empty_database(self):
        """
        Check that the view correctly handles an empty db.
        """
        self.authenticate()
        response = self.client.get(reverse('recipe-random'))
        self.assertEqual(response.status_code, 200)
    
    def test_random_recipe_view_200(self):
        self.authenticate()
        recipe = Recipe(**self.recipe_data)
        recipe.save()
        response = self.client.get(reverse('recipe-random'))
        self.assertEqual(response.status_code, 200)

class RecipeSearchRandomViewTest(CookboxBaseTest):
    def test_requires_auth(self):
        response = self.client.get(reverse('recipe-search-random'))
        self.assertEqual(response.status_code, 302)

    def test_recipe_search_random_view_200(self):
        self.authenticate()
        response = self.client.get(reverse('recipe-search-random'))
        self.assertEqual(response.status_code, 200)
