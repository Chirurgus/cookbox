# Created by Oleksandr Sorochynskyi
# On 06/12/2019

from django.urls import path, reverse_lazy, include
from django.contrib.auth.views import LogoutView

from cookbox_recipeui import urls as RecipeUI_urls

from .views import (
    HomePageView,
    CustomLoginView,
    TagList,
    TagRecipeList,
    TagEdit,
    TagDelete,
    TagCreate,
    TagCategoryCreate,
    TagCategoryEdit,
    TagCategoryDelete,
)

# Don't require authentication for the login page
login_view = CustomLoginView.as_view()
login_view.auth_exempt = True

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("login")), name="logout"),
    path("tags/", TagList.as_view(), name="tag-list"),
    path("tags/<int:pk>/recipes/", TagRecipeList.as_view(), name="tag-recipe-list"),
    path("tags/create/", TagCreate.as_view(), name="tag-create"),
    path("tags/edit/<int:pk>/", TagEdit.as_view(), name="tag-edit"),
    path("tags/delete/<int:pk>/", TagDelete.as_view(), name="tag-delete"),
    path(
        "tags/create_category/", TagCategoryCreate.as_view(), name="tag-category-create"
    ),
    path(
        "tags/edit_category/<int:pk>/",
        TagCategoryEdit.as_view(),
        name="tag-category-edit",
    ),
    path(
        "tags/delete_category/<int:pk>/",
        TagCategoryDelete.as_view(),
        name="tag-category-delete",
    ),
    path("recipes/", include(RecipeUI_urls)),
]
