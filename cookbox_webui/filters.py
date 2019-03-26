import django.forms.widgets as widgets

from dal.autocomplete import ModelSelect2Multiple

from django_filters import FilterSet, ModelMultipleChoiceFilter

from cookbox_core.models import Recipe, Tag

class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name= 'tags__name',
        to_field_name= 'name',
        queryset= Tag.objects.all(),
        widget= widgets.CheckboxSelectMultiple()
    )

    class Meta:
        model = Recipe
        fields = {
            'name' : ['icontains'],
            'source' : ['icontains'],
            'total_time': ['lt', 'gt'],
        }
