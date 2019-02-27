# Generated by Django 2.1.2 on 2019-02-26 18:55

from django.db import migrations

def make_tags_unique(apps, schema_editor):
    Tag = apps.get_model("cookbox_core", "Tag")

    unique_tag_names = { tag.name for tag in Tag.objects.all() }

    for tag_name in unique_tag_names:
        # Create one (unique) tag with this name
        new_tag = Tag(name=tag_name)
        # Save it to get an id
        new_tag.save()

        # Go though all the tags with same name
        for tag in Tag.objects.filter(name=tag_name):
            # Add the recipes to the new tag
            new_tag.recipes.add(tag.recipe)
            # Remove the old tag
            tag.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cookbox_core', '0006_auto_20190226_1954'),
    ]

    operations = [
        migrations.RunPython(make_tags_unique)
    ]
