from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("store", "0004_alter_product_product_type")]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_negotiable_price",
            field=models.BooleanField(default=False, verbose_name="Договорная цена"),
        ),
    ]
