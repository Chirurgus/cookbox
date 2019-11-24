# Created by Oleksandr Sorochynskyi
# On 17/11/2019

from django.db import transaction
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
    ValidationError,
)
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import CheckboxSelectMultiple

from django_superform.forms import SuperModelFormMixin
from django_superform import InlineFormSetField

from .models import GlossaryEntry, GlossarySynonym


class GlossarySynonymForm(ModelForm):
    class Meta:
        model = GlossarySynonym
        fields = ['synonym']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['synonym'].widget.attrs.update({'placeholder': 'Synonym'})

class GlossarySynonymBaseFormset(BaseInlineFormSet):
    def save(self, commit=True):
        instances = super().save(commit=False)
        if not commit:
            return instances
        old_synonyms = set([ s.synonym for s in self.instance.synonyms.all() ])
        new_synonyms = set([ s.synonym for s in instances ])
        # Synonyms to be deleted
        for synonym in old_synonyms.difference(new_synonyms):
            GlossarySynonym.objects.get(synonym=synonym).delete()
        # Synonyms to be created
        for synonym in new_synonyms.difference(old_synonyms):
            GlossarySynonym.objects.create(entry=self.instance, synonym=synonym)
        return instances
    
GlossarySynonymFormset = inlineformset_factory(
    parent_model=GlossaryEntry,
    model=GlossarySynonymForm.Meta.model,
    form=GlossarySynonymForm,
    formset=GlossarySynonymBaseFormset,
    extra=0
)

class GlossaryEntryForm(SuperModelFormMixin, ModelForm):
    synonyms = InlineFormSetField(formset_class=GlossarySynonymFormset)

    class Meta:
        model = GlossaryEntry
        fields = ['title', 'text']
    
    class Media:
        js = ( "cookbox_webui/js/dynamic_forms.js", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'placeholder': 'Entry title'}
        )

