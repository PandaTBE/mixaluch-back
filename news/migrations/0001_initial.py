# Generated by Django 4.1.1 on 2023-06-12 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="News",
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
                ("name", models.CharField(max_length=128)),
                ("short_text", models.CharField(default="", max_length=512)),
                ("is_important", models.BooleanField(default=False)),
                ("markdown_text", models.TextField(default="", null=True)),
                (
                    "image",
                    models.ImageField(
                        default="images/default.png",
                        help_text="Upload news image",
                        upload_to="images/news/",
                        verbose_name="News image",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "News",
                "verbose_name_plural": "News",
            },
        ),
    ]
