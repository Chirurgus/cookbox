from django.urls import include, path

from rest_framework import routers

from .views import RecipeViewSet

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]