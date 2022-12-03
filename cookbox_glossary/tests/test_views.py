# Created by Oleksandr Sorochynskyi
# On 03/12/2019

from django.test import Client
from django.urls import reverse, reverse_lazy

from cookbox_glossary.models import (
    GlossaryArticle,
    GlossaryEntry,
)
from cookbox_glossary.views import insert_links

from .base import GlossaryBaseTest


class GlossaryViewTest(GlossaryBaseTest):
    def test_requires_auth(self):
        response = self.client.get(reverse("glossary"))
        self.assertRedirects(
            response, reverse("login") + "?next=" + reverse("glossary")
        )

    def test_glossary_200(self):
        self.authenticate()
        response = self.client.get(reverse("glossary"))
        self.assertEqual(response.status_code, 200)


class EntryDetailViewTest(GlossaryBaseTest):
    def test_requires_auth(self):
        entry = GlossaryEntry(**self.entry_data)
        entry.save()
        path = reverse("glossary-entry-detail", kwargs={"pk": entry.pk})
        response = self.client.get(path)
        self.assertRedirects(response, reverse("login") + "?next=" + path)

    def test_entry_detail_200(self):
        self.authenticate()
        entry = GlossaryEntry(**self.entry_data)
        entry.save()
        path = reverse("glossary-entry-detail", kwargs={"pk": entry.pk})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


class EntryCreateViewTest(GlossaryBaseTest):
    def test_requires_auth(self):
        path = reverse("glossary-entry-create")
        response = self.client.get(path)
        self.assertRedirects(response, reverse("login") + "?next=" + path)

    def test_entry_detail_200(self):
        self.authenticate()
        path = reverse("glossary-entry-create")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


class EntryEditViewTest(GlossaryBaseTest):
    def test_requires_auth(self):
        entry = GlossaryEntry(**self.entry_data)
        entry.save()
        path = reverse("glossary-entry-edit", kwargs={"pk": entry.pk})
        response = self.client.get(path)
        self.assertRedirects(response, reverse("login") + "?next=" + path)

    def test_entry_detail_200(self):
        self.authenticate()
        entry = GlossaryEntry(**self.entry_data)
        entry.save()
        path = reverse("glossary-entry-edit", kwargs={"pk": entry.pk})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


class EntryDeleteViewTest(GlossaryBaseTest):
    def test_requires_auth(self):
        entry = GlossaryEntry(**self.entry_data)
        entry.save()
        path = reverse("glossary-entry-delete", kwargs={"pk": entry.pk})
        response = self.client.get(path)
        self.assertRedirects(response, reverse("login") + "?next=" + path)

    def test_entry_detail_200(self):
        self.authenticate()
        entry = GlossaryEntry(**self.entry_data)
        entry.save()
        path = reverse("glossary-entry-delete", kwargs={"pk": entry.pk})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


class ArticleCreateViewTest(GlossaryBaseTest):
    def test_requires_auth(self):
        path = reverse("glossary-article-create")
        response = self.client.get(path)
        self.assertRedirects(response, reverse("login") + "?next=" + path)

    def test_article_detail_200(self):
        self.authenticate()
        path = reverse("glossary-article-create")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


class ArticleEditViewTest(GlossaryBaseTest):
    def test_requires_auth(self):
        article = GlossaryArticle(**self.article_data)
        article.save()
        path = reverse("glossary-article-edit", kwargs={"pk": article.pk})
        response = self.client.get(path)
        self.assertRedirects(response, reverse("login") + "?next=" + path)

    def test_article_detail_200(self):
        self.authenticate()
        article = GlossaryArticle(**self.article_data)
        article.save()
        path = reverse("glossary-article-edit", kwargs={"pk": article.pk})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


class ArticleDeleteViewTest(GlossaryBaseTest):
    def test_requires_auth(self):
        article = GlossaryArticle(**self.article_data)
        article.save()
        path = reverse("glossary-article-delete", kwargs={"pk": article.pk})
        response = self.client.get(path)
        self.assertRedirects(response, reverse("login") + "?next=" + path)

    def test_article_detail_200(self):
        self.authenticate()
        article = GlossaryArticle(**self.article_data)
        article.save()
        path = reverse("glossary-article-delete", kwargs={"pk": article.pk})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
