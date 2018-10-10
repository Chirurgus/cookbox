"""cookbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, reverse_lazy
#from rest_framework import routers
from cb_database.views import RecipeList, RecipeDetail, RecipeNew
from django.contrib.auth.views import LoginView, LogoutView

#router = routers.DefaultRouter()
#router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('recipes/', RecipeList.as_view(), name= 'recipe-list'),
    path('recipes/<int:pk>/', RecipeDetail.as_view(), name= 'recipe-edit'),
    path('recipes/create/', RecipeNew.as_view(), name= 'recipe-create'),
    path('login/', LoginView.as_view(template_name= 'login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page= reverse_lazy('login')), name='logout'),
    path('admin/', admin.site.urls),
    path('_nested_admin/', include('nested_admin.urls')),
    #path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
