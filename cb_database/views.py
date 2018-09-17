from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic.detail import DetailView

from rest_framework import viewsets

from .forms import *
from .models import Recipe
from .serializers import RecipeSerializer

# API endpoint that allows recipes to be viewed or edited.
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeList(View):
    template_name = 'recipe_list.html'

    def get(self, request, *args, **kwargs):
        queryset = Recipe.objects.all()
        return render(request, self.template_name, {'recipes': queryset})

#class RecipeDetailView(DetailView):
    #model = Recipe
class RecipeDetail(View):
    template_name = 'recipe_detail.html'

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        recipe_form = RecipeForm(instance= recipe, prefix="recipe")
        time_info_form = TimeInfoForm(instance= recipe, prefix= "time_info")
        yield_info_form = YieldInfoForm(instance= recipe, prefix= "yield_info")

        ingredient_groups_form = IngredientGroupFormset(instance= recipe,
                                                        prefix= "ingredient_groups")
        instructions_form = InstructionFormset(instance = recipe,
                                               prefix= "instructions")
        notes_form = RecipeNoteFormset(instance = recipe, prefix= 'notes')
        tag_form = TagFormset(instance= recipe, prefix= 'tags')

        recipe_forms = { 'recipe'    : recipe_form,
                         'time_info' : time_info_form,
                         'yield_info': yield_info_form
                       } 
        inlines = { 'ingredient_groups' : ingredient_groups_form,
                    'instructions'      : instructions_form,
                    'notes'             : notes_form,
                    'tags'              : tag_form
                  }
        return render(request, self.template_name, {'recipe': recipe,
                                                    'recipe_forms': recipe_forms,
                                                    'inlines' : inlines})


    def post(self, request, pk):
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/recipes-list/')
        else:
            return render(request, self.template_name, {'form' : form})