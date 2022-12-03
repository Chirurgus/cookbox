# Created by Oleksandr Sorochynskyi
# On 06/12/2019

"""
Cookbox URL Configuration
"""

from django.urls import include, path

from cookbox_webui import urls as WebUI_urls
from cookbox_admin import urls as Admin_urls


urlpatterns = [
    path("", include(WebUI_urls)),
    path("admin/", include(Admin_urls)),
]

# If DEBUG is True, then serve media files from here
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
