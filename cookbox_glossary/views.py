# Created by Oleksandr Sorochynskyi
# On 25/07/2019

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

from markdownx.utils import markdownify

from .models import (
    GlossarySynonym,
    GlossaryEntry,
)
from .forms import GlossaryEntryForm

def insert_links(html):
    '''
    Replace all occurrences of words found in the Cookbox Glossary
    by a link to the page of that term Wikipedia style.

    :param str html: String in which to find and replace the glossary terms.
    :return: String with all glossary terms replaced.
    '''
    ancor_link = '<a href="{link}">{term}</a>'
    for entry in GlossaryEntry.objects.all():
        link = reverse('glossary-entry', kwargs={ 'pk': entry.id })
        terms = [ synonym.synonym for synonym in entry.synonyms.all() ]
        terms.append(entry.title)
        for term in terms:
            html = html.replace(term, ancor_link.format(link=link, term=term))
    return html

class GlossaryView(ListView):
    template_name = 'cookbox_glossary/list.html'
    model = GlossaryEntry
    context_object_name = "glossary"
    
class GlossaryEntryView(DetailView):
    template_name = 'cookbox_glossary/detail.html'
    model = GlossaryEntry
    context_object_name = "entry"

    def get_object(self):
        entry = super().get_object()
        # Format markdown
        entry.formatted_markdown =  mark_safe(insert_links(markdownify(entry.text)))
        return entry

class GlossaryEntryCreateView(CreateView):
    template_name = 'cookbox_glossary/edit.html'
    model = GlossaryEntry
    fields = ['title']
    context_object_name = 'entry'
    success_url = reverse_lazy('glossary')
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

class GlossaryEntryEditView(UpdateView):
    template_name = 'cookbox_glossary/edit.html'
    model = GlossaryEntry
    context_object_name = 'entry'
    success_url = reverse_lazy('glossary')
    form_class = GlossaryEntryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = False
        return context
    
class GlossaryEntryDeleteView(DeleteView):
    template_name = 'delete.html' # Use delete template from webui
    model = GlossaryEntry
    success_url = reverse_lazy('glossary')
    context_object_name = 'entry'
