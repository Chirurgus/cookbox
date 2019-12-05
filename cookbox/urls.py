"""
cookbox URL Configuration

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
from django.contrib.auth.views import LoginView, LogoutView

from cookbox_webui import urls as WebUI_urls
from cookbox_admin import urls as Admin_urls
from cookbox_glossary import urls as Glossary_urls
from cookbox_seasons import urls as Seasons_urls


urlpatterns = [
    path('', include(WebUI_urls)),
    path('admin/', include(Admin_urls)),
    path('glossary/', include(Glossary_urls)),
    path('seasons/', include(Seasons_urls)),
    # Load urls for 
    path('markdownx/', include('markdownx.urls')),
]

# If DEBUG is True, then serve media files from here
from django.conf import settings
from django.conf.urls.static import static

if (settings.DEBUG):
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)