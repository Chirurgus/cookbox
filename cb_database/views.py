from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, View

from .forms import RecipeCompleteForm
from .models import Recipe
from .serializers import RecipeSerializer

'''
# API endpoint that allows recipes to be viewed or edited.
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    '''

class RecipeList(ListView):
    template_name = 'recipe_list.html'
    queryset = Recipe.objects.all()
    context_object_name = 'recipes'

class RecipeDetail(View):
    template_name = 'recipe_detail.html'

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
            return HttpResponseRedirect('recipe-list')
        else:
            return render(request,
                          self.template_name,
                          {'recipe'  : recipe,
                           'form'    : form })
