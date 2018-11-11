import random

from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from cookbox_core.models import Recipe

from .forms import RecipeCompleteForm


class BaseLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')

class RecipeList(BaseLoginRequiredMixin, View):
    template_name = 'recipe_list.html'

    def get(self, request):
        queryset = Recipe.objects.all()

        return render(request,
                      self.template_name,
                      {'recipes' : queryset })

class RecipeDetail(BaseLoginRequiredMixin, View):
    template_name = 'recipe_detail.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        return render(request,
                      self.template_name,
                      { 'recipe' : recipe })

class RecipeNew(BaseLoginRequiredMixin, View):
    template_name = 'recipe_edit.html'

    def get(self, request):
        recipe_form = RecipeCompleteForm()

        return render(request,
                      self.template_name,
                      { 'form' : recipe_form,
                        'new'  : True })

    # PUT method is not allowed for HTML forms, so POST is used even for new instances
    def post(self, request):
        recipe_form = RecipeCompleteForm(data= request.POST)

        if recipe_form.is_valid():
            recipe_form.create()
            return HttpResponseRedirect(reverse('recipe-list'))
        else:
            return render(request,
                          self.template_name,
                          { 'form' : recipe_form,
                            'new'  : True  })

class RecipeEdit(BaseLoginRequiredMixin, View):
    template_name = 'recipe_edit.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        recipe_form = RecipeCompleteForm(instance= recipe)

        return render(request,
            self.template_name,
            {'recipe'    : recipe,
             'form'      : recipe_form})

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        form = RecipeCompleteForm(data= request.POST, instance= recipe)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('recipe-list'))
        else:
            return render(request,
                          self.template_name,
                          {'recipe'  : recipe,
                           'form'    : form })

class RecipeDelete(BaseLoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-list')
    template_name = 'recipe_delete.html'

def recipe_random(request):
    ids = Recipe.objects.values_list('id', flat= True)
    rand_id = random.choice(ids)
    return HttpResponseRedirect(reverse('recipe-detail',kwargs= {'pk': rand_id}))
