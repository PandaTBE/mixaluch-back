from config import HOST_URL
from rest_framework import serializers

from .models import Product, ProductImage, ProductExternalId


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = ProductImage
        fields = "__all__"

    def validate(self, attrs):
        if self.instance is None and "image" not in attrs:
            raise serializers.ValidationError({"image": "Загрузите изображение."})
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {**data, "image": f"{HOST_URL}{instance.image.url}" if instance.image else None}


class ProductExternalIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductExternalId
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    product_image = ImageSerializer(many=True, read_only=True)
    external_ids = ProductExternalIdSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "category",
            "regular_price",
            "is_negotiable_price",
            "product_image",
            "unit",
            "min_quantity",
            "external_ids",
            "is_popular",
            "slug",
            "discount_price",
        ]


class ProductCardSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "title", "description", "category", "regular_price",
            "discount_price", "is_negotiable_price", "product_image", "unit",
            "min_quantity", "is_popular", "slug",
        ]

    def get_product_image(self, obj):
        images = list(obj.product_image.all())
        main = next((image for image in images if image.is_feature), None)
        if main is None and images:
            main = images[0]
        return ImageSerializer([main], many=True).data if main else []
