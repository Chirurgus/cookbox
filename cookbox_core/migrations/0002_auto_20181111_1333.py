# Generated by Django 2.1.2 on 2018-11-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbox_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
