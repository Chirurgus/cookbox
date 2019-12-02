# Created by Oleksandr Sorochynskyi
# On 17/11/2019

from django.db import transaction
from django.forms import (
    ModelForm,
    ModelMultipleChoiceField,
)
from django.forms.widgets import CheckboxSelectMultiple

from dal.autocomplete import ModelSelect2Multiple

from .models import GlossaryEntry, GlossaryArticle


class GlossaryEntryForm(ModelForm):
    class Meta:
        model = GlossaryEntry
        fields = ['term']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['term'].widget.attrs.update({'placeholder': 'Glossary term'})
    
class GlossaryArticleForm(ModelForm):
    terms = ModelMultipleChoiceField(queryset= GlossaryEntry.objects.all(),
                                     widget= ModelSelect2Multiple(url= 'glossary-entry-autocomplete'),
                                     required= False)

    class Meta:
        model = GlossaryArticle
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        article = kwargs.get('instance')
        if article is not None:
            self.fields['terms'].initial = article.entries.all()
        else:
            self.fields['terms'].inital = []
    
    def save(self, commit=True):
        '''
        '''
        with transaction.atomic():
            ret = super().save(commit)
            if commit:
                self.save_terms()
            return ret
    
    def save_terms(self):
        '''
        Saves terms many2many field.
        Gets called automatically from save(commit=True) method.
        '''
        self.instance.entries.set(self.cleaned_data['terms'])
    
 
