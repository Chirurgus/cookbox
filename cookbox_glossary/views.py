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
    GlosarrySynonym,
    GlossaryEntry,
)

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
        entry.formatted_markdown =  mark_safe(markdownify(entry.text))
        return entry

class GlossaryEntryCreateView(CreateView):
    template_name = 'cookbox_glossary/edit.html'
    model = GlossaryEntry
    fields = ['title']
    context_object_name = 'entry'
    success_url = reverse_lazy('glossary')
   
class GlossaryEntryEditView(UpdateView):
    template_name = 'cookbox_glossary/edit.html'
    model = GlossaryEntry
    fields = ['title', 'text']
    context_object_name = 'entry'
    success_url = reverse_lazy('glossary')

class GlossaryEntryDeleteView(DBaseLoginRequiredMixin, eleteView):
    template_name = 'delete.html' # Use delete template from webui
    model = GlossaryEntry
    success_url = reverse_lazy('glossary')
    context_object_name = 'entry'
