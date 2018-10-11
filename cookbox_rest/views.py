from django.shortcuts import render

from cookbox_core.models import Recipe

from .serializers import RecipeSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    ''' API endpoint that allows recipes to be viewed or edited. '''
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
