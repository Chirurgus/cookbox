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
        time_info_form = TimeInfoForm(post, instance= recipe, prefix= "time_info")
        yield_info_form = YieldInfoForm(post, instance= recipe, prefix= "yield_info")

        ingredient_groups_form = IngredientGroupFormset(post,
                                                        instance= recipe, prefix= "ingredient_groups")
        instructions_form = InstructionFormset(post,
                                               instance= recipe, prefix= "instructions")
        notes_form = RecipeNoteFormset(post, instance= recipe, prefix= 'notes')
        tag_form = TagFormset(post, instance= recipe, prefix= 'tags')
        recipe_forms = { 'recipe'    : recipe_form,
                         'time_info' : time_info_form,
                         'yield_info': yield_info_form
                       } 
        inlines = { 'ingredient_groups' : ingredient_groups_form,
                    'instructions'      : instructions_form,
                    'notes'             : notes_form,
                    'tags'              : tag_form
                  }
        return { 'forms' : recipe_forms, 'inlines' : inlines}


    def get_recipe_forms(self, recipe):
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
        return { 'forms' : recipe_forms, 'inlines' : inlines}

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        recipe_forms = self.get_recipe_forms(recipe)
        
        return render(request,
            self.template_name,
            {'recipe'       : recipe,
             'recipe_forms' : recipe_forms['forms'],
             'inlines'      : recipe_forms['inlines'] })


    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        forms = self.recipe_forms_post(request.POST,recipe)
        valid = True
        for key,form in forms['forms'].items():
            valid = valid and form.is_valid()
        for key,form in forms['inlines'].items():
            valid = valid and form.is_valid()
        if valid:
            for key,form in forms['forms'].items():
                form.save()
            for key,form in forms['inlines'].items():
                form.save()
            return HttpResponseRedirect('/recipe-list')
        else:
            return render(request,
                          self.template_name,
                          {'recipe'       : recipe,
                          'recipe_forms' : forms['forms'],
                          'inlines'      : forms['inlines'] })
