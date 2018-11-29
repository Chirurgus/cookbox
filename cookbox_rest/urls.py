from django.urls import include, path

from cookbox_rest.views import (
    RecipeListAPIView,
    RecipeDetailAPIView
)


urlpatterns = [
    path('recipes/', RecipeListAPIView.as_view()),
    path('recipes/<int:pk>/', RecipeDetailAPIView.as_view()),
]