# Generated by Django 2.2.6 on 2019-12-05 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SeasonsItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=256)),
                ("note", models.CharField(default="", max_length=1024)),
                (
                    "jan",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "feb",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "mar",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "apr",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "may",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "jun",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "jul",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "aug",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "sep",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "oct",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "nov",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                (
                    "dec",
                    models.CharField(
                        choices=[
                            ("peak", "Peak season"),
                            ("in", "In season"),
                            ("out", "Out of season"),
                        ],
                        default="out",
                        max_length=126,
                    ),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
