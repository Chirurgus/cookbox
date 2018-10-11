from django.contrib import admin
from django.urls import include, path, reverse_lazy

urlpatterns = [
    path('/', admin.site.urls),
    path('_nested_admin/', include('nested_admin.urls')),
]