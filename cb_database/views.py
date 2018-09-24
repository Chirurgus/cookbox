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

    def recipe_forms_post(self, post, recipe):
        recipe_form = RecipeForm(post, instance= recipe, prefix="recipe")

        ingredient_groups_form = IngredientGroupFormset(post,
                                                        instance= recipe, prefix= "ingredient_groups")
        instructions_form = InstructionFormset(post,
                                               instance= recipe, prefix= "instructions")
        notes_form = RecipeNoteFormset(post, instance= recipe, prefix= 'notes')
        tag_form = TagFormset(post, instance= recipe, prefix= 'tags')
        inlines = { 'ingredient_groups' : ingredient_groups_form,
                    'instructions'      : instructions_form,
                    'notes'             : notes_form,
                    'tags'              : tag_form
                  }
        return { 'form' : recipe_form, 'inlines' : inlines}


    def get_recipe_forms(self, recipe):
        recipe_form = RecipeForm(instance= recipe, prefix="recipe")

        ingredient_groups_form = IngredientGroupFormset(instance= recipe,
                                                        prefix= "ingredient_groups")
        instructions_form = InstructionFormset(instance = recipe,
                                               prefix= "instructions")
        notes_form = RecipeNoteFormset(instance = recipe, prefix= 'notes')
        tag_form = TagFormset(instance= recipe, prefix= 'tags')
        inlines = { 'ingredient_groups' : ingredient_groups_form,
                    'instructions'      : instructions_form,
                    'notes'             : notes_form,
                    'tags'              : tag_form
                  }
        return { 'form' : recipe_form, 'inlines' : inlines}

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
            return HttpResponseRedirect('/recipe-list')
        else:
            return render(request,
                          self.template_name,
                          {'recipe'  : recipe,
                           'form'    : form })
