from django.shortcuts import render

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView 
)

from cookbox_core.models import Recipe

from .serializers import RecipeSerializer


class RecipeListAPIView(ListCreateAPIView):
    '''
    API endpoint that shows a list of recipes, and handles createion of new recipes
    '''
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeDetailAPIView(RetrieveUpdateDestroyAPIView):
    ''' 
    API endpoint that allows for CURD operations on individual recipes
    '''
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
