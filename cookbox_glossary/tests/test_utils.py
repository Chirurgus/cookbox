# Created by Oleksandr Sorochynskyi
# On 06/12/2019

from django.urls import reverse

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
        # Initialize an entry with an article
        article = GlossaryArticle(**self.article_data)
        article.save()
        entry = GlossaryEntry(**self.entry_data)
        entry.article = article
        entry.save()
        # Get the link to the entry (with article)
        link = reverse('glossary-entry-detail', kwargs={ 'pk': entry.id })
        # Compare expectation vs acutal result
        result = insert_links(entry.term)
        expectation = '<a href="{link}">{term}</a>'.format(link=link, term=entry.term)
        self.assertEqual(result, expectation)


