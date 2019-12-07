# Created by Oleksandr Sorochynskyi
# On 04/12/2019

from django.urls import reverse,reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import SeasonsItem

class SeasonsListView(ListView):
    template_name = 'cookbox_seasons/list.html'
    model = SeasonsItem
    context_object_name = 'items'
    queryset = SeasonsItem.objects.all().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PEAK_SEASON'] = SeasonsItem.PEAK_SEASON
        context['IN_SEASON'] = SeasonsItem.IN_SEASON
        context['OUT_OF_SEASON'] = SeasonsItem.OUT_OF_SEASON
        return context

class SeasonsItemEditBaseViewMixin(object):
    template_name = 'cookbox_seasons/edit.html'
    model = SeasonsItem
    context_object_name = 'item'
    success_url = reverse_lazy('seasons')
    fields = [
        'name',
        'note',
        'jan', 'feb', 'mar', 'apr', 'may', 'jun',
        'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
    ]

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        form.fields['note'].required = False
        return form

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
    model = SeasonsItem
    success_url = reverse_lazy('seasons')
    context_object_name = 'item'
