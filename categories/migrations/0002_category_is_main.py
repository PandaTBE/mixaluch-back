# Generated by Django 4.1.1 on 2023-12-07 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="is_main",
            field=models.BooleanField(default=False),
        ),
    ]
