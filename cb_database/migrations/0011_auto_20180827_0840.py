# Generated by Django 2.1 on 2018-08-27 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cb_database', '0010_auto_20180827_0827'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['position']},
        ),
        migrations.AlterModelOptions(
            name='ingredientgroup',
            options={'ordering': ['position']},
        ),
        migrations.AlterModelOptions(
            name='instruction',
            options={'ordering': ['position']},
        ),
        migrations.AddField(
            model_name='ingredient',
            name='position',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='ingredientgroup',
            name='position',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='instruction',
            name='position',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]