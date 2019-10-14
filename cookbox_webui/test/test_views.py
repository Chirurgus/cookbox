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
from cookbox_core.tests import CookboxBaseTest

class TagListViewTest(CookboxBaseTest):
    def test_tag_list_view_200(self):
        response = self.client.get(reverse('tag-list'))

        self.assertEqual(response.status_code, 200)
       
class TagCreateViewTest(CookboxBaseTest):
    def test_tag_create_view_200(self):
        response = self.client.get(reverse('tag-create'))
        self.assertEqual(response.status_code, 200)

class TagEditViewTest(CookboxBaseTest):
    def test_tag_edit_view_200(self):
        tag = Tag(**self.tag_data).save()
        response = self.client.get(
            reverse('tag-edit', kwargs= {'pk' : tag.id })
        )
        self.assertEqual(response.status_code, 200)

class TagCategoryCreateViewTest(CookboxBaseTest):
    def test_tag_category_create_view_200(self):
        response = self.client.get(reverse('tag-category-create'))

        self.assertEqual(response.status_code, 200)

class TagCategoryEditViewTest(CookboxBaseTest):
    def test_tag_category_edit_view_200(self):
        tag_category = TagCategory(**self.tag_category_data).save()
        response = self.client.get(
            reverse('tag-category-edit', kwargs= {'pk' : tag_category.id })
        )
        self.assertEqual(response.status_code, 200)

class TagCategoryDeleteViewTest(CookboxBaseTest):
    def test_tag_category_delete_view_200(self):
        tag_category = TagCategory(**self.tag_category_data).save()
        response = self.client.get(
            reverse('tag-category-delete', kwargs= {'pk' : tag_category.id })
        )
        self.assertEqual(response.status_code, 200)
