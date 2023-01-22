# Generated by Django 4.1.1 on 2023-01-22 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_alter_order_order_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="email",
        ),
        migrations.RemoveField(
            model_name="order",
            name="second_name",
        ),
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.CharField(blank=True, default="", max_length=1000),
        ),
        migrations.AddField(
            model_name="order",
            name="comment",
            field=models.CharField(blank=True, default="", max_length=3000),
        ),
        migrations.AddField(
            model_name="order",
            name="delivery_cost",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="order",
            name="delivery_type",
            field=models.CharField(
                choices=[
                    ("SELF_DELIVERY", "Самовывоз"),
                    ("COURIER_DELIVERY", "Курьером"),
                ],
                default="COURIER_DELIVERY",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_type",
            field=models.CharField(
                choices=[("CASH_PAYMENT", "Наличными"), ("CARD_PAYMENT", "Картой")],
                default="CARD_PAYMENT",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="products_total",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="order",
            name="total",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
