from django.contrib import admin
from django.urls import include, path, reverse_lazy

from .views import (
    GlossaryListView,
    GlossaryArticleCreateView,
    GlossaryArticleEditView,
    GlossaryArticleDeleteView,
    GlossaryEntryDetailView,
    GlossaryEntryCreateView,
    GlossaryEntryEditView,
    GlossaryEntryDeleteView,
    GlossaryTermsAutocomplete,
)

urlpatterns = [
    path('', GlossaryListView.as_view(), name="glossary"),
    path('entry/create/', GlossaryEntryCreateView.as_view(), name="glossary-entry-create"),
    path('entry/autocomplete/', GlossaryTermsAutocomplete.as_view(), name="glossary-entry-autocomplete"),
    path('entry/<slug:pk>/', GlossaryEntryDetailView.as_view(), name="glossary-entry-detail"),
    path('entry/<slug:pk>/edit/', GlossaryEntryEditView.as_view(), name="glossary-entry-edit"),
    path('entry/<slug:pk>/delete/', GlossaryEntryDeleteView.as_view(), name="glossary-entry-delete"),
    path('article/create/', GlossaryArticleCreateView.as_view(), name="glossary-article-create"),
    path('article/<slug:pk>/edit/', GlossaryArticleEditView.as_view(), name="glossary-article-edit"),
    path('article/<slug:pk>/delete/', GlossaryArticleDeleteView.as_view(), name="glossary-article-delete"),
]