# Generated by Django 4.1.1 on 2022-09-27 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_cartitem_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cartitem",
            old_name="price",
            new_name="total_price",
        ),
    ]
