from django.contrib import admin
from django.urls import include, path, reverse_lazy

from .views import (
    GlossaryView,
    GlossaryEntryView,
    GlossaryEntryCreateView,
    GlossaryEntryEditView,
    GlossaryEntryDeleteView,
)

urlpatterns = [
    path('', GlossaryView.as_view(), name="glossary"),
    path('entry/create/', GlossaryEntryCreateView.as_view(), name="glossary-entry-create"),
    path('entry/<slug:pk>/', GlossaryEntryView.as_view(), name="glossary-entry"),
    path('entry/<slug:pk>/edit/', GlossaryEntryEditView.as_view(), name="glossary-entry-edit"),
    path('entry/<slug:pk>/delete/', GlossaryEntryDeleteView.as_view(), name="glossary-entry-delete"),
]