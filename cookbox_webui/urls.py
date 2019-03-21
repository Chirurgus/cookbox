from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    RecipeList,
    RecipeDetail,
    RecipeEdit,
    RecipeNew,
    RecipeDelete,
    RecipeImport,
    RecipeTagAutocomplete,
    TagList,
    TagEdit,
    TagCreate,
    recipe_random,
)

urlpatterns = [
    path('login/', LoginView.as_view(template_name= 'login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page= reverse_lazy('login')), name='logout'),
    path('', RecipeList.as_view(), name= 'recipe-list'),
    path('<int:pk>/', RecipeDetail.as_view(), name= 'recipe-detail'),
    path('import/', RecipeImport.as_view(), name= 'recipe-import'),
    path('edit/<int:pk>/', RecipeEdit.as_view(), name= 'recipe-edit'),
    path('create/', RecipeNew.as_view(), name= 'recipe-create'),
    path('delete/<int:pk>/', RecipeDelete.as_view(), name= 'recipe-delete'),
    path('random/', recipe_random, name= 'recipe-random'),
    path('recipe-tag-autocomplete', RecipeTagAutocomplete.as_view(), name="recipe-tag-autocomplete"),
    path('tags/', TagList.as_view(), name="tag-list"),
    path('tags/edit/<int:pk>', TagEdit.as_view(), name="tag-edit"),
    path('tags/create', TagCreate.as_view(), name="tag-create"),
]
