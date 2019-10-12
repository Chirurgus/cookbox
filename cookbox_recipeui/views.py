# Created by Oleksandr Sorochynskyi
# On 12/10/2019

import random

from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    View,
    DeleteView,
)
from django.core.paginator import Paginator

from dal.autocomplete import Select2QuerySetView

from cookbox_scraper import WebsiteNotImplementedError

from cookbox_core.models import Recipe

from cookbox_scraper import scrape, supported_hosts

from cookbox_webui.views import BaseLoginRequiredMixin

from .forms import RecipeForm, SearchForm


class RecipeList(BaseLoginRequiredMixin, View):
    template_name = 'cookbox_recipeui/list.html'

    def get(self, request):
        qs = Recipe.objects.all().order_by("-last_modified")
        paginator = Paginator(qs, 20)
        page = request.GET.get('page') or 1
        recipes = paginator.get_page(page)
        return render(request,
                      self.template_name,
                      {'recipes' : recipes })

class RecipeDetail(BaseLoginRequiredMixin, View):
    template_name = 'cookbox_recipeui/detail.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        return render(request,
                      self.template_name,
                      { 'recipe' : recipe })


class RecipeCreate(BaseLoginRequiredMixin, View):
    template_name = 'cookbox_recipeui/edit.html'

    def get(self, request):
        recipe_form = RecipeForm()

        return render(request,
                      self.template_name,
                      { 'form' : recipe_form,
                        'new'  : True })

    # PUT method is not allowed for HTML forms,
    # so POST is used even for new instances
    def post(self, request):
        recipe_form = RecipeForm(data= request.POST)

        if recipe_form.is_valid():
            recipe_form.save()
            return HttpResponseRedirect(reverse('recipe-list'))
        else:
            return render(request,
                          self.template_name,
                          { 'form' : recipe_form,
                            'new'  : True  })

class RecipeImport(BaseLoginRequiredMixin, View):
    template_name = 'cookbox_recipeui/import.html'

    submit_button_name = 'import-url'

    def get(self, request):
        return render(request,
                      self.template_name,
                      {'supported_hosts'    : supported_hosts(),
                       'submit_button_name' : self.submit_button_name})

    def post(self, request):
        import_url = request.POST.get(self.submit_button_name, None)
        try:
            recipe = scrape(import_url)
            return HttpResponseRedirect(
                reverse('recipe-edit',
                        kwargs= { 'pk': recipe.id }))

        except WebsiteNotImplementedError:
            return render(request,
                      self.template_name,
                      {'supported_hosts'    : supported_hosts(),
                       'submit_button_name' : self.submit_button_name,
                       'error'              : 'This domain is not supported' })

class RecipeEdit(BaseLoginRequiredMixin, View):
    template_name = 'cookbox_recipeui/edit.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        recipe_form = RecipeForm(instance= recipe)

        return render(request,
            self.template_name,
            {'recipe'    : recipe,
             'form'      : recipe_form})

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        form = RecipeForm(data= request.POST,
                                files= request.FILES,
                                instance= recipe)
    

        if form.is_valid():
            recipe = form.save()

        # Re-render the form if there are errors or user
        # wants to continue editing (in this case submit button
        # has name "_continue" and this is in the POST dict.)
        if not form.is_valid():
                return render(request,
                            self.template_name,
                            {'recipe'  : recipe,
                            'form'    : form })

        if "_continue" in request.POST:
            return HttpResponseRedirect(
                reverse('recipe-edit',
                        kwargs= {'pk': pk}))

        return HttpResponseRedirect(
            reverse('recipe-detail',
                    kwargs= {'pk': pk}))

class RecipeDelete(BaseLoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-list')
    template_name = 'delete.html'

class RecipeTagAutocomplete(Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs

class RecipeSearch(BaseLoginRequiredMixin, View):
    template_name = 'cookbox_recipeui/search.html'
    
    def get(self, request):
        return render(request,
                      self.template_name,
                      { 'search_form' : SearchForm() })
    
    def post(self, request):
        search = SearchForm(data= request.POST)

        if search.is_valid():
            qs = Recipe.objects.all()
            if not search.cleaned_data['name'] is None:
                qs = qs.filter(
                    name__icontains = search.cleaned_data['name']
                )
            if not search.cleaned_data['source'] is None:
                qs = qs.filter(
                    source__icontains = search.cleaned_data['source']
                )
            if not search.cleaned_data['max_duration'] is None:
                qs = qs.filter(
                    total_time__lt = search.cleaned_data['max_duration']
                )
            if not search.cleaned_data['min_duration'] is None: 
                qs = qs.filter(
                    total_time__gt = search.cleaned_data['min_duration']
                )
            return render(request,
                          'cookbox_recipeui/list.html',
                          { 'recipes'       : qs,
                            'no_pagination' : True })
        else:
            return render(request,
                          self.template_name,
                          { 'search_form' : search })

def recipe_random_search(request):
    search = SearchForm(data= request.POST)

    if search.is_valid():
        qs = Recipe.objects.all()
        if not search.cleaned_data['name'] is None:
            qs = qs.filter(
                name__icontains = search.cleaned_data['name']
            )
        if not search.cleaned_data['source'] is None:
            qs = qs.filter(
                source__icontains = search.cleaned_data['source']
            )
        if not search.cleaned_data['max_duration'] is None:
            qs = qs.filter(
                total_time__lt = search.cleaned_data['max_duration']
            )
        if not search.cleaned_data['min_duration'] is None: 
            qs = qs.filter(
                total_time__gt = search.cleaned_data['min_duration']
            )
        id = random.choice(qs).id
        return HttpResponseRedirect(reverse('recipe-detail',
                                    kwargs= {'pk': id }))
    else:
        return render(request,
                        "cookbox_recipeui/search.html",
                        { 'search_form' : search })

def recipe_random(request):
    ids = Recipe.objects.values_list('id', flat= True)
    rand_id = random.choice(ids)
    return HttpResponseRedirect(reverse('recipe-detail',
                                kwargs= {'pk': rand_id}))
