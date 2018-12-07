from django.http import Http404

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from cookbox_core.models import Recipe

from .serializers import RecipeSerializer



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'recipes': reverse('api-recipe-list', request=request, format=format),
    })

class RecipeListAPIView(APIView):
    '''
    API endpoint that shows a list of recipes, and handles createion of new recipes
    '''
    serializer_class = RecipeSerializer

    def get(self, request, format=None):
        recipes = Recipe.objects.all()
        fields = request.GET.get('fields', None)
        if fields is not None:
            fields = fields.split(',')
        serializer = self.serializer_class(recipes, fields= fields, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecipeDetailAPIView(APIView):
    ''' 
    API endpoint that allows for CURD operations on individual recipes
    '''
    serializer_class = RecipeSerializer

    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        recipe = self.get_object(pk)
        fields = request.GET.get('fields', None)
        if fields is not None:
            fields = fields.split(',')
        serializer = self.serializer_class(recipe, fields=fields)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        recipe = self.get_object(pk)
        serializer = self.serializer_class(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        recipe = self.get_object(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
