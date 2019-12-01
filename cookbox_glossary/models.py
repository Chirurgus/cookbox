# Created by Oleksandr Sorochynskyi
# On 24/07/2019

from django.db import models

from markdownx.models import MarkdownxField

from cookbox_core.models import CHAR_FIELD_MAX_LEN_MEDIUM

class GlossaryArticle(models.Model):
    body = MarkdownxField()
    last_modified = models.DateTimeField(auto_now=True)
    # Additional related fields
    # entries

class GlossaryEntry(models.Model):
    term = models.CharField(max_length=CHAR_FIELD_MAX_LEN_MEDIUM, null=False, blank=False)
    article = models.ForeignKey(GlossaryArticle, on_delete=models.CASCADE, related_name="entries")

    def save(self, *args, **kwargs):
        self.term = self.term.lower()
        super().save(*args, **kwargs)
