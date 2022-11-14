# Generated by Django 4.1.1 on 2022-11-14 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_product_display_on_home_page"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="display_on_home_page",
        ),
        migrations.AddField(
            model_name="product",
            name="is_popular",
            field=models.BooleanField(default=False, verbose_name="Is popular?"),
        ),
    ]
