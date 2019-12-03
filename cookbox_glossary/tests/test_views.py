# Created by Oleksandr Sorochynskyi
# On 03/12/2019

from django.test import Client
from django.urls import reverse,reverse_lazy

from cookbox_glossary.models import (
    GlossaryArticle,
    GlossaryEntry,
)
from cookbox_glossary.views import insert_links


from .base import GlossaryBaseTest



class GlossaryInsertLinksTest(GlossaryBaseTest):
    '''
    Test 'cookbox_glossary.views.insert_links' function.
    '''
    def test_does_noting_if_empty(self):
        before = "A long test string, with many words"
        after = insert_links(before)
        self.assertEqual(before, after)

    def test_replaces(self):
        entry
        before = "A long test string, with many words"
        after = insert_links(before)
        self.assertEqual(before, after)


class GlossaryViewTest(GlossaryBaseTest):
    def test_requires_auth(self):
        response = self.client.get(reverse('glossary'))
        self.assertRedirects(
            response,
            reverse('login') + "?next=" + reverse('glossary')
        )
    
    def test_glossary_200(self):
        self.authenticate()
        response = self.client.get(reverse('glossary'))
        self.assertEqual(response.status_code, 200)

class EntryDetailViewTest(GlossaryBaseTest):
    def test_requires_auth(self):
        entry = GlossaryEntry(**self.entry_data)
        entry.save()
        path = reverse('glossary-entry-detail', kwargs={'pk' : entry.pk})
        response = self.client.get(path)
        self.assertRedirects(response,
            reverse('login') + "?next=" + path
        )
    
    def test_entry_detail_200(self):
        self.authenticate()
        entry = GlossaryEntry(**self.entry_data)
        entry.save()
        path = reverse('glossary-entry-detail', kwargs={'pk' : entry.pk})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


# Entry detail
# Entry create
# Entr edit
# entry delete
# article create
# Article edit
# Article delete
# Entry term autocomplete