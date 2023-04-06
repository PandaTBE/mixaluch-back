from config import HOST_URL
from rest_framework import serializers

from .models import Product, ProductImage


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = ProductImage
        fields = "__all__"

    def get_image_url(self, obj):
        return f"{HOST_URL}{obj.image.url}"


class ProductSerializer(serializers.ModelSerializer):
    product_image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "title", "description", "category", "regular_price",
            "product_image", "unit", "min_quantity"
        ]
