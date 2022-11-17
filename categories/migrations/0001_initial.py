# Generated by Django 4.1.1 on 2022-11-16 14:40

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Обязательное и уникальное",
                        max_length=255,
                        unique=True,
                        verbose_name="Название категории",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        max_length=255,
                        unique=True,
                        verbose_name="Уникальный адрес для категории",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "image",
                    models.ImageField(
                        default="images/default.png",
                        help_text="Добавьте изображении категории",
                        upload_to="images/categories",
                        verbose_name="Изображении категории",
                    ),
                ),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="categories.category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
    ]