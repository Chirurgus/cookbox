from rest_framework import viewsets
from .serializers import RecipeSerializer
from .models import Recipe

# API endpoint that allows recipes to be viewed or edited.
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


