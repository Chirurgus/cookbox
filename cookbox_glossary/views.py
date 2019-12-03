# Created by Oleksandr Sorochynskyi
# On 25/07/2019

import re

from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe

from dal.autocomplete import Select2QuerySetView

from markdownx.utils import markdownify

from .models import (
    GlossaryArticle,
    GlossaryEntry,
)
from .forms import GlossaryEntryForm, GlossaryArticleForm

def insert_links(html, ignore=set()):
    '''
    Replace all occurrences of words found in the Cookbox Glossary
    by a link to the page of that term Wikipedia style.

    :param str html: String in which to find and replace the glossary terms.
    :param set of str: set of terms not to replace
    :return: String with all glossary terms replaced.
    '''
    ancor_link = '<a href="{link}">{term}</a>'
    for article in GlossaryArticle.objects.all():
        for entry in article.entries.all():
            term = entry.term
            if term in ignore:
                continue
            link = reverse('glossary-entry-detail', kwargs={ 'pk': entry.id })
            expr = re.compile(re.escape(term), re.IGNORECASE)
            html = expr.sub(ancor_link.format(link=link, term=term), html)
    return html

class GlossaryListView(ListView):
    template_name = 'cookbox_glossary/list.html'
    model = GlossaryEntry
    context_object_name = "entries"
    queryset = GlossaryEntry.objects.all().order_by("term")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orphaned_articles'] = GlossaryArticle.objects.filter(entries__isnull=True)
        return context
    
class GlossaryEntryDetailView(DetailView):
    template_name = 'cookbox_glossary/entry/detail.html'
    model = GlossaryEntry
    context_object_name = "entry"

    def get_object(self):
        entry = super().get_object()
        if entry.article is not None:
            # Format markdown
            entry.formatted_markdown =  mark_safe(
                insert_links(
                    markdownify(entry.article.body),
                    entry.term
                )
            )
        return entry

class GlossaryEntryCreateView(CreateView):
    template_name = 'cookbox_glossary/entry/edit.html'
    model = GlossaryEntry
    context_object_name = 'entry'
    success_url = reverse_lazy('glossary')
    fields = ['term']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

class GlossaryEntryEditView(UpdateView):
    template_name = 'cookbox_glossary/entry/edit.html'
    model = GlossaryEntry
    context_object_name = 'entry'
    success_url = reverse_lazy('glossary')
    fields = ['term']
    
class GlossaryEntryDeleteView(DeleteView):
    template_name = 'delete.html' # Use delete template from webui
    model = GlossaryEntry
    success_url = reverse_lazy('glossary')
    context_object_name = 'entry'

class GlossaryArticleCreateView(CreateView):
    template_name = 'cookbox_glossary/article/edit.html'
    model = GlossaryArticle
    context_object_name = 'article'
    form_class = GlossaryArticleForm

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        if 'entry' in self.request.GET:
            id = self.request.GET['entry']
            entry = GlossaryEntry.objects.get(pk=id)
            form.fields['terms'].initial |=  entry
        return form
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

    def get_success_url(self):
        if 'entry' in self.request.GET:
            id = self.request.GET['entry']
            return reverse('glossary-entry-detail', kwargs= { 'pk': id })
        else:
            return reverse('glossary')

class GlossaryArticleEditView(UpdateView):
    template_name = 'cookbox_glossary/article/edit.html'
    model = GlossaryArticle
    context_object_name = 'article'
    form_class = GlossaryArticleForm

    def get_success_url(self):
        if self.object.entries.all():
            id = self.object.entries.first().id
            return reverse('glossary-entry-detail', kwargs= { 'pk': id })
        else:
            return reverse('glossary')

class GlossaryArticleDeleteView(DeleteView):
    template_name = 'delete.html' # Use delete template from webui
    model = GlossaryArticle
    success_url = reverse_lazy('glossary')
    context_object_name = 'article'

class GlossaryTermsAutocomplete(Select2QuerySetView):
    create_field = 'term'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return GlossaryEntry.objects.none()

        qs = GlossaryEntry.objects.all().order_by("term")

        if self.q:
            qs = qs.filter(term__icontains=self.q)

        return qs

