# Created by Oleksandr Sorochynskyi
# On 06/12/2019

from django.test import Client
from django.urls import reverse, reverse_lazy

from cookbox_seasons.models import SeasonsItem

from .base import SeasonsBaseTest


class SeasonsItemListViewTest(SeasonsBaseTest):
    def test_requires_auth(self):
        response = self.client.get(reverse("seasons"))
        self.assertRedirects(response, reverse("login") + "?next=" + reverse("seasons"))

    def test_200(self):
        self.authenticate()
        response = self.client.get(reverse("seasons"))
        self.assertEqual(response.status_code, 200)


class SeasonsItemCreateViewTest(SeasonsBaseTest):
    def test_requires_auth(self):
        response = self.client.get(reverse("seasons-item-create"))
        self.assertRedirects(
            response, reverse("login") + "?next=" + reverse("seasons-item-create")
        )

    def test_200(self):
        self.authenticate()
        response = self.client.get(reverse("seasons-item-create"))
        self.assertEqual(response.status_code, 200)


class SeasonsItemEditViewTest(SeasonsBaseTest):
    def test_requires_auth(self):
        item = SeasonsItem(**self.seasons_item_data)
        item.save()
        response = self.client.get(reverse("seasons-item-edit", kwargs={"pk": item.id}))
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("seasons-item-edit", kwargs={"pk": item.id}),
        )

    def test_200(self):
        self.authenticate()
        item = SeasonsItem(**self.seasons_item_data)
        item.save()
        response = self.client.get(reverse("seasons-item-edit", kwargs={"pk": item.id}))
        self.assertEqual(response.status_code, 200)


class SeasonsItemDeleteViewTest(SeasonsBaseTest):
    def test_requires_auth(self):
        item = SeasonsItem(**self.seasons_item_data)
        item.save()
        response = self.client.get(
            reverse("seasons-item-delete", kwargs={"pk": item.id})
        )
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("seasons-item-delete", kwargs={"pk": item.id}),
        )

    def test_200(self):
        self.authenticate()
        item = SeasonsItem(**self.seasons_item_data)
        item.save()
        response = self.client.get(
            reverse("seasons-item-delete", kwargs={"pk": item.id})
        )
        self.assertEqual(response.status_code, 200)
