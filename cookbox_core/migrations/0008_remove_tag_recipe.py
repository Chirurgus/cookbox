# Generated by Django 2.1.2 on 2019-03-02 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookbox_core', '0007_auto_20190226_1955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='recipe',
        ),
    ]
