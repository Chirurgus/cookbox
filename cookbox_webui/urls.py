from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    RecipeList,
    RecipeDetail,
    RecipeSearch,
    RecipeEdit,
    RecipeCreate,
    RecipeDelete,
    RecipeImport,
    RecipeTagAutocomplete,
    TagList,
    TagEdit,
    TagDelete,
    TagCreate,
    TagCategoryCreate,
    TagCategoryEdit,
    TagCategoryDelete,
    recipe_random,
    recipe_random_search,
)

urlpatterns = [
    path('login/', LoginView.as_view(template_name= 'login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page= reverse_lazy('login')), name='logout'),
    path('', RecipeList.as_view(), name= 'recipe-list'),
    path('<int:pk>/', RecipeDetail.as_view(), name= 'recipe-detail'),
    path('search/', RecipeSearch.as_view(), name='recipe-search'),
    path('search_random/', recipe_random_search, name='recipe-search-random'),
    path('import/', RecipeImport.as_view(), name= 'recipe-import'),
    path('edit/<int:pk>/', RecipeEdit.as_view(), name= 'recipe-edit'),
    path('create/', RecipeCreate.as_view(), name= 'recipe-create'),
    path('delete/<int:pk>/', RecipeDelete.as_view(), name= 'recipe-delete'),
    path('random/', recipe_random, name= 'recipe-random'),
    path('recipe-tag-autocomplete/', RecipeTagAutocomplete.as_view(), name="recipe-tag-autocomplete"),
    path('tags/', TagList.as_view(), name="tag-list"),
    path('tags/create/', TagCreate.as_view(), name="tag-create"),
    path('tags/edit/<int:pk>/', TagEdit.as_view(), name="tag-edit"),
    path('tags/delete/<int:pk>/', TagDelete.as_view(), name="tag-delete"),
    path('tags/create_category/', TagCategoryCreate.as_view(), name="tag-category-create"),
    path('tags/edit_category/<int:pk>/', TagCategoryEdit.as_view(), name="tag-category-edit"),
    path('tags/delete_category/<int:pk>/', TagCategoryDelete.as_view(), name="tag-category-delete"),
]
