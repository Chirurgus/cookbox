# Created by Oleksandr Sorochynskyi
# On 12/10/2019

from django.urls import path

from .views import (
    RecipeList,
    RecipeDetail,
    RecipeEdit,
    RecipeCreate,
    RecipeDelete,
    RecipeImport,
    RecipeTagAutocomplete,
    RecipeSearch,
    recipe_random,
    recipe_random_search,
)

urlpatterns = [
    path('', RecipeList.as_view(), name= 'recipe-list'),
    path('<int:pk>/', RecipeDetail.as_view(), name= 'recipe-detail'),
    path('import/', RecipeImport.as_view(), name= 'recipe-import'),
    path('edit/<int:pk>/', RecipeEdit.as_view(), name= 'recipe-edit'),
    path('create/', RecipeCreate.as_view(), name= 'recipe-create'),
    path('delete/<int:pk>/', RecipeDelete.as_view(), name= 'recipe-delete'),
    path('recipe-tag-autocomplete/', RecipeTagAutocomplete.as_view(), name="recipe-tag-autocomplete"),
    path('random/', recipe_random, name= 'recipe-random'),
    path('search/', RecipeSearch.as_view(), name='recipe-search'),
    path('search_random/', recipe_random_search, name='recipe-search-random'),
]
