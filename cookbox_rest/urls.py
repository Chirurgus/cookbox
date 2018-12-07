from django.urls import include, path, re_path

from cookbox_rest.views import (
    RecipeListAPIView,
    RecipeDetailAPIView,
    api_root
)


urlpatterns = [
    path('', api_root, name="api-root"),
    path('recipes/', RecipeListAPIView.as_view(), name="api-recipe-list"),
    path('recipes/<int:pk>/', RecipeDetailAPIView.as_view(), name="api-recipe-detail"),
]