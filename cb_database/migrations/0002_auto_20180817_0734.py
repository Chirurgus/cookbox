# Generated by Django 2.1 on 2018-08-17 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cb_database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=256)),
                ('total_time', models.DecimalField(decimal_places=2, max_digits=12)),
                ('preparation_time', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('cook_time', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='YieldInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=256)),
                ('total_yield', models.CharField(max_length=256)),
                ('serving_size', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='recipe',
            name='source',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='basicingredient',
            name='description',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='recipe',
            name='time',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='cb_database.TimeInfo'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='yield_size',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='cb_database.YieldInfo'),
        ),
    ]
