# Generated by Django 2.1.1 on 2018-10-11 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ingredient",
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
                ("unit", models.CharField(max_length=256)),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=12)),
                ("description", models.CharField(default="", max_length=256)),
                ("usda_code", models.PositiveIntegerField(blank=True, null=True)),
                ("position", models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                "ordering": ["position"],
            },
        ),
        migrations.CreateModel(
            name="IngredientGroup",
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
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("position", models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                "ordering": ["position"],
            },
        ),
        migrations.CreateModel(
            name="IngredientNote",
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
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "text",
                    models.CharField(blank=True, default="", max_length=256, null=True),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notes",
                        to="cookbox_core.Ingredient",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Instruction",
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
                ("instruction", models.CharField(default="", max_length=256)),
                ("position", models.PositiveSmallIntegerField(null=True)),
            ],
            options={
                "ordering": ["position"],
            },
        ),
        migrations.CreateModel(
            name="InstructionNote",
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
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "text",
                    models.CharField(blank=True, default="", max_length=256, null=True),
                ),
                (
                    "instruction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notes",
                        to="cookbox_core.Instruction",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Recipe",
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
                ("description", models.CharField(default="", max_length=256)),
                ("unit_time", models.CharField(max_length=256)),
                ("total_time", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "preparation_time",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "cook_time",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("unit_yield", models.CharField(max_length=256)),
                ("total_yield", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "serving_size",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("source", models.CharField(blank=True, default="", max_length=256)),
                ("last_modified", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="RecipeNote",
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
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "text",
                    models.CharField(blank=True, default="", max_length=256, null=True),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notes",
                        to="cookbox_core.Recipe",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Tag",
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
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tags",
                        to="cookbox_core.Recipe",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="instruction",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="instructions",
                to="cookbox_core.Recipe",
            ),
        ),
        migrations.AddField(
            model_name="ingredientgroup",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_groups",
                to="cookbox_core.Recipe",
            ),
        ),
        migrations.AddField(
            model_name="ingredient",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredients",
                to="cookbox_core.IngredientGroup",
            ),
        ),
    ]
