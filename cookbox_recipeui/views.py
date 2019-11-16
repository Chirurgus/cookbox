# Created by Oleksandr Sorochynskyi
# On 12/10/2019

import random

from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    FormView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.paginator import Paginator

from dal.autocomplete import Select2QuerySetView

import cookbox_scraper as scraper

from cookbox_core.models import Recipe, Tag

from .forms import RecipeForm, SearchForm, ImportRecipeForm


class RecipeList(ListView):
    template_name = 'cookbox_recipeui/list.html'
    queryset = Recipe.objects.all().order_by("-last_modified") 
    context_object_name = "recipes"
    paginate_by = 24

class RecipeDetail(DetailView):
    template_name = 'cookbox_recipeui/detail.html'
    model = Recipe
    context_object_name = "recipe"

class RecipeCreate(CreateView):
    template_name = 'cookbox_recipeui/edit.html'
    model = Recipe
    context_object_name = "recipe"
    form_class = RecipeForm
    success_url = reverse_lazy('recipe-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

class RecipeImport(FormView):
    template_name = 'cookbox_recipeui/import.html'
    form_class = ImportRecipeForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supported_hosts'] = scraper.supported_hosts()
        return context

    def form_valid(self, form):
        import_url = form.cleaned_data['url']
        recipe = scraper.scrape(import_url)
        return HttpResponseRedirect(
            reverse('recipe-edit', kwargs= { 'pk': recipe.id })
        )

class RecipeEdit(UpdateView):
    template_name = 'cookbox_recipeui/edit.html'
    model = Recipe
    context_object_name = "recipe"
    form_class = RecipeForm

    def form_valid(self, form):
        recipe = form.save()
        if '_continue' in self.request.POST.keys():
            return HttpResponseRedirect(
                reverse(
                    'recipe-edit',
                    kwargs= { 'pk': recipe.id }
                )
            )
        else:
            return HttpResponseRedirect(
                reverse(
                    'recipe-detail',
                    kwargs= { 'pk': recipe.id }
                )
            )


class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-list')
    template_name = 'delete.html'

class RecipeTagAutocomplete(Select2QuerySetView):
    create_field = 'name'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

class RecipeSearch(FormView):
    template_name = 'cookbox_recipeui/search.html'
    form_class = SearchForm
    
    def form_valid(self, form):
        qs = form.filtered_qs()
        return render(
            self.request,
            'cookbox_recipeui/list.html',
            { 'recipes' : qs, 'no_pagination' : True }
        )

def recipe_random_search(request):
    search = SearchForm(data= request.POST)

    if search.is_valid():
        qs = search.filtered_qs()
        if (len(qs) > 0):
            id = random.choice(qs).id
            return HttpResponseRedirect(
                reverse('recipe-detail', kwargs= {'pk': id })
            )
        else:
            return render(
                request,
                'cookbox_recipeui/list.html',
                { 'recipes' : qs, 'no_pagination' : True }
            )
    else:
        return render(request,
                        "cookbox_recipeui/search.html",
                        { 'search_form' : search })

def recipe_random(request):
    ids = Recipe.objects.values_list('id', flat= True)
    if (len(ids) > 0):
        rand_id = random.choice(ids)
        return HttpResponseRedirect(reverse('recipe-detail',
                                    kwargs= {'pk': rand_id}))
    else:
        return render(
                request,
                'cookbox_recipeui/list.html',
                { 'recipes' : [], 'no_pagination' : True }
        )
        
