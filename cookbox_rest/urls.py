from django.urls import include, path, re_path

from cookbox_rest.views import (
    RecipeListAPIView,
    RecipeDetailAPIView,
    api_root
)


urlpatterns = [
    path('', api_root, name="api-root"),
    path('recipes/', RecipeListAPIView.as_view(), name="api-recipe-list"),
    re_path(r'recipes/(?P<pk>\d+)(?:\?fields=(?P<fields>\w+(?:,\w+)*)?)?/$', RecipeDetailAPIView.as_view(), name="api-recipe-detail"),
]