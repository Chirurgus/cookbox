# Generated by Django 4.1.3 on 2025-02-16 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookbox_glossary', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='glossaryentry',
            name='article',
        ),
        migrations.DeleteModel(
            name='GlossaryArticle',
        ),
        migrations.DeleteModel(
            name='GlossaryEntry',
        ),
    ]
