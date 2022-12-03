# Created by Oleksandr Sorochynskyi
# On 05/12/2019

from django.urls import path

from .views import (
    SeasonsListView,
    SeasonsItemCreateView,
    SeasonsItemEditView,
    SeasonsItemDeleteView,
)

urlpatterns = [
    path("", SeasonsListView.as_view(), name="seasons"),
    path("item/create/", SeasonsItemCreateView.as_view(), name="seasons-item-create"),
    path(
        "item/<slug:pk>/edit/", SeasonsItemEditView.as_view(), name="seasons-item-edit"
    ),
    path(
        "item/<slug:pk>/delete/",
        SeasonsItemDeleteView.as_view(),
        name="seasons-item-delete",
    ),
]
