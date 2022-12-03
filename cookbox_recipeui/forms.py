# Created by Oleksandr Sorochynskyi
# On 12/10/2019

"""
Forms for interacting with Recipe objects.
"""

import six

from django.db import transaction
from django.db.models import F
from django.forms import (
    Form,
    ModelForm,
    BaseInlineFormSet,
    inlineformset_factory,
    modelformset_factory,
    ModelMultipleChoiceField,
    Textarea,
    CharField,
    FloatField,
    ChoiceField,
    URLField,
    ValidationError,
)
from django.forms.widgets import CheckboxSelectMultiple

from django_superform.forms import SuperModelFormMixin, SuperModelFormMetaclass
from django_superform import InlineFormSetField

from dal.autocomplete import ModelSelect2Multiple

from cookbox_core.models import (
    Recipe,
    IngredientGroup,
    Ingredient,
    Instruction,
    RecipeNote,
    IngredientNote,
    InstructionNote,
    Tag,
    CHAR_FIELD_MAX_LEN_SHORT,
)

import cookbox_scraper as scraper

from .widgets import ImageWidget


class CookboxInlineFormset(BaseInlineFormSet):
    """
    Allows to change the prefix string of the empty_form via
    `self.empty_form_prefix`.

    Forms are added to formsets on the client-side by replacing
    '__prefix__' string in the empty_form html. This does not
    work for nested formsets since the empty_form will contain
    the empty_form for the nested formset. By changing the
    '__prefix__' to something else for every formset class we
    ensure that only the correct __prefix__'s are replaced.
    """

    empty_form_prefix = "__prefix__"

    # Just copies the definition form BaseInlineFormSet
    # but replaces the hard-coded '__prefix__' by a variable
    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix(self.empty_form_prefix),
            empty_permitted=True,
            use_required_attribute=False,
            **self.get_form_kwargs(None)
        )
        self.add_fields(form, None)
        return form


class ModelFormWithInlineFormsetMixin(object):
    """
    Allow nested forms to be automatically saved.

    If a form containing an InlineFormset is dynamically created on the
    client the forms in the formset will not have an id of their parent
    (because it doesn't have one yet). This means that we first need to save
    the parent form and only then the child form can be saved. However, by
    default, the forms first saves its children, and only then saves the
    parent. This is why this class has to be used to save children an
    additional time after the parent has been saved.

    Deleted forms should not be saved, since their instance would already be
    deleted by super().save().
    """

    def save(self, commit=True):
        """
        (Re)saves the related formsets, so that newly created
        nested formsets are also saved.
        """
        # Save the parent
        ret = super().save(commit)
        if hasattr(self, "formsets"):
            for formset in self.formsets.values():
                for form in formset.forms:
                    if not form in formset.deleted_forms:
                        form.save(commit)
        return ret


class NoteForm(ModelForm):
    class Meta:
        abstract = True
        fields = ["text", "image"]
        widgets = {
            "image": ImageWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update({"placeholder": "Note text"})


class NoteInlineFormset(CookboxInlineFormset):
    empty_form_prefix = "__note_prefix__"


class InstructionNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = InstructionNote
        abstract = False


InstructionNoteFormset = inlineformset_factory(
    parent_model=Instruction,
    model=InstructionNoteForm.Meta.model,
    form=InstructionNoteForm,
    formset=NoteInlineFormset,
    extra=0,
)


class IngredientNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = IngredientNote
        abstract = False


IngredientNoteFormset = inlineformset_factory(
    parent_model=Ingredient,
    model=IngredientNoteForm.Meta.model,
    form=IngredientNoteForm,
    formset=NoteInlineFormset,
    extra=0,
)


class RecipeNoteForm(NoteForm):
    class Meta(NoteForm.Meta):
        model = RecipeNote
        abstract = False


RecipeNoteFormset = inlineformset_factory(
    parent_model=Recipe,
    model=RecipeNoteForm.Meta.model,
    form=RecipeNoteForm,
    formset=NoteInlineFormset,
    extra=0,
)


class IngredientForm(
    six.with_metaclass(
        SuperModelFormMetaclass,
        SuperModelFormMixin,
        ModelFormWithInlineFormsetMixin,
        ModelForm,
    )
):
    notes = InlineFormSetField(formset_class=IngredientNoteFormset)

    class Meta:
        model = Ingredient
        fields = ["position", "quantity", "unit", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity"].widget.attrs.update({"placeholder": "Quantity"})
        self.fields["unit"].widget.attrs.update({"placeholder": "Unit"})
        self.fields["description"].widget.attrs.update({"placeholder": "Ingredient"})


class IngredientInlineFormset(CookboxInlineFormset):
    empty_form_prefix = "__ingredient_prefix__"


IngredientFormset = inlineformset_factory(
    parent_model=IngredientGroup,
    model=IngredientForm.Meta.model,
    form=IngredientForm,
    formset=IngredientInlineFormset,
    extra=0,
)


class IngredientGroupForm(
    six.with_metaclass(
        SuperModelFormMetaclass,
        SuperModelFormMixin,
        ModelFormWithInlineFormsetMixin,
        ModelForm,
    )
):
    ingredients = InlineFormSetField(formset_class=IngredientFormset)

    class Meta:
        model = IngredientGroup
        fields = ["position", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Ingredient group"})


class IngredientGroupInlineFormset(CookboxInlineFormset):
    empty_form_prefix = "__ingredient_group_prefix__"


IngredientGroupFormset = inlineformset_factory(
    parent_model=Recipe,
    model=IngredientGroupForm.Meta.model,
    form=IngredientGroupForm,
    formset=IngredientGroupInlineFormset,
    extra=0,
)


class InstructionForm(
    six.with_metaclass(
        SuperModelFormMetaclass,
        SuperModelFormMixin,
        ModelFormWithInlineFormsetMixin,
        ModelForm,
    )
):
    notes = InlineFormSetField(formset_class=InstructionNoteFormset)

    class Meta:
        model = Instruction
        fields = ["position", "instruction"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["instruction"].widget.attrs.update({"placeholder": "Instruction"})


class InstructionInlineFormset(CookboxInlineFormset):
    empty_form_prefix = "__instruction_prefix__"


InstructionFormset = inlineformset_factory(
    parent_model=Recipe,
    model=InstructionForm.Meta.model,
    form=InstructionForm,
    formset=InstructionInlineFormset,
    extra=0,
)


class RecipeForm(
    six.with_metaclass(
        SuperModelFormMetaclass,
        SuperModelFormMixin,
        ModelFormWithInlineFormsetMixin,
        ModelForm,
    )
):
    ingredient_groups = InlineFormSetField(formset_class=IngredientGroupFormset)
    instructions = InlineFormSetField(formset_class=InstructionFormset)
    notes = InlineFormSetField(formset_class=RecipeNoteFormset)
    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=ModelSelect2Multiple(url="recipe-tag-autocomplete"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        recipe = kwargs.get("instance")
        if recipe is not None:
            self.fields["tags"].initial = recipe.tags.all()
        else:
            self.fields["tags"].inital = []

    def save(self, commit=True):
        """
        Same as ModelForm.save(), but also saves tags if commit=True
        """
        with transaction.atomic():
            ret = super().save(commit)
            if commit:
                self.save_tags()
            return ret

    def save_tags(self):
        """
        Saves tags many2many field.
        Gets called automatically from save(commit=True) method.
        """
        self.instance.tags.set(self.cleaned_data["tags"])

    class Media:
        css = {"all": ("cookbox_recipeui/css/recipe_form.css",)}
        js = (
            "cookbox_webui/js/dynamic_forms.js",
            "cookbox_webui/js/jquery.are-you-sure-1.9.0.js",
            "cookbox_recipeui/js/recipe_form.js",
            "cookbox_recipeui/js/html5sortable.min.js",
        )

    class Meta:
        model = Recipe
        fields = [
            "name",
            "description",
            "unit_time",
            "total_time",
            "preparation_time",
            "cook_time",
            "unit_yield",
            "total_yield",
            "serving_size",
            "source",
            "image",
            "tags",
        ]
        labels = {
            "name": "Recipe name",
            "unit_time": "Time measurement unit",
            "unit_yield": "Yield measurement unit",
        }
        widgets = {
            "description": Textarea(attrs={}),
            "image": ImageWidget(),
        }


class SearchForm(Form):
    name = CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, required=False)
    source = CharField(max_length=CHAR_FIELD_MAX_LEN_SHORT, required=False)
    duration_unit = ChoiceField(choices=Recipe.TIME_UNITS)
    max_duration = FloatField(required=False)
    min_duration = FloatField(required=False)

    @staticmethod
    def _convert_time(x, unit_in, unit_out):
        # Convert the unit to days, then convert to desired unit
        days_coef = {
            Recipe.SEC: 1 / 86400,
            Recipe.MIN: 1 / 1440,
            Recipe.HRS: 1 / 24,
            Recipe.DAYS: 1,
            Recipe.WEEKS: 7,
            Recipe.MONTH: 365.5 / 12,
            Recipe.YEAR: 365.5,
        }

        if unit_in not in days_coef.keys() or unit_out not in days_coef.keys():
            raise ValueError(
                "Time units have to be one of the time units supported by Recipe"
            )

        return x * (days_coef[unit_in] / days_coef[unit_out])

    def filtered_qs(self):
        """
        Filter the Recipes that respond to the search.
        """
        qs = Recipe.objects.all()
        if self.cleaned_data["name"] is not None:
            qs = qs.filter(name__icontains=self.cleaned_data["name"])
        if self.cleaned_data["source"] is not None:
            qs = qs.filter(source__icontains=self.cleaned_data["source"])
        if self.cleaned_data["max_duration"] is not None:
            ids = [
                r.id
                for r in qs
                if r.total_time
                <= SearchForm._convert_time(
                    self.cleaned_data["max_duration"],
                    self.cleaned_data["duration_unit"],
                    r.unit_time,
                )
            ]
            qs = qs.filter(id__in=ids)
        if self.cleaned_data["min_duration"] is not None:
            ids = [
                r.id
                for r in qs
                if r.total_time
                >= SearchForm._convert_time(
                    self.cleaned_data["min_duration"],
                    self.cleaned_data["duration_unit"],
                    r.unit_time,
                )
            ]
            qs = qs.filter(id__in=ids)
        return qs


class ImportRecipeForm(Form):
    url = URLField(label="Recipe URL", required=True)
