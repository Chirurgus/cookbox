# Created by Oleksandr Sorochynskyi
# On 04/12/2019

from django.urls import reverse,reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import SeasonItem

class SeasonsListView(ListView):
    template_name = 'cookbox_seasons/list.html'
    model = SeasonItem
    context_object_name = 'items'
    queryset = SeasonItem.objects.all().order_by("name")

class SeasonsItemEditBaseViewMixin(object):
    template_name = 'cookbox_seasons/edit.html'
    model = SeasonItem
    context_object_name = 'items'
    success_url = reverse_lazy('seasons')
    fields = [
        'name',
        'description',
        'jan', 'feb', 'mar', 'apr', 'may', 'jun',
        'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
    ]

class SeasonsItemCreateView(SeasonsItemEditBaseViewMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

class SeasonsItemEditView(SeasonsItemEditBaseViewMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = False
        return context

class SeasonsItemDeleteView(DeleteView):
    template_name = 'delete.html' # Use delete template from webui
    model = SeasonItem
    success_url = reverse_lazy('seasons')
    context_object_name = 'item'
