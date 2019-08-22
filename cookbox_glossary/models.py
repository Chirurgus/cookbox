# Created by Oleksandr Sorochynskyi
# On 24/07/2019

from django.db import models

from markdownx.models import MarkdownxField

from cookbox_core.models import CHAR_FIELD_MAX_LEN_MEDIUM

class GlossaryEntry(models.Model):
    title = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM, null=False, blank=False)
    text = MarkdownxField()
    last_modified = models.DateTimeField(auto_now=True)
    # Additional related fields
    # synonyms

class GlosarrySynonym(models.Model):
    entry = models.ForeignKey(GlossaryEntry, on_delete=models.CASCADE, related_name="synonyms")
    synonym = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM)


