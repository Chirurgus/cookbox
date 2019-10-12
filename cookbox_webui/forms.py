# Created by Oleksandr Sorochynskyi
# On 22/09/2019

"""
Forms for the Web UI of Cookbox.

Forms in this file can be divided into 3 groups: Recipe,
Tag, and Search.
Recipe forms are all the forms of Recipes or its components 
and build up to RecipeForm which is used to create/edit
recipes. Forms for the recipe components (eg. IngredientForm)
can be used on their own in principle. Tag forms are for
creating and editing tags. Finally SearchForm is a simple form
to gather information for searching for recipes.

RecipeForm is composed of its own fields on top of formsets
for forms for recipe components. To achieve this while retaining
the same interface as the standard ModelForm two thigs were
required:
    - Superforms to include formsets as fields
    - CookboxInlineFormset allows for dynamic replication
      of nested formsets
    - ModelFormWithInlineFormsetMixin to save the nested formsets
"""
from django.forms import (
    ModelForm,
    Form,
    modelformset_factory,
    ModelChoiceField,
    ModelMultipleChoiceField,
)


from cookbox_core.models import (
    Tag,
    TagCategory,
)



class TagForm(ModelForm):
    category = ModelChoiceField(queryset= TagCategory.objects.all(),
                                required= False)

    class Meta:
        model = Tag
        fields = ['name', 'category']

class TagCategoryForm(ModelForm):
    class Meta:
        model = TagCategory
        fields = ['name']
