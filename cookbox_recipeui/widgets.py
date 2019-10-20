# Created by Oleksandr Sorochynskyi
# On 19/10/2019

from django.forms.widgets import ClearableFileInput


class ImageWidget(ClearableFileInput):
    template_name = "cookbox_recipeui/widgets/image_widget.html"
