from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0009_order_delivery_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderingSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("notice", models.CharField(blank=True, default="", max_length=500)),
                ("self_delivery_enabled", models.BooleanField(default=True)),
                ("courier_delivery_enabled", models.BooleanField(default=True)),
            ],
        ),
    ]
