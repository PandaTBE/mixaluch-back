from config import HOST_URL
from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    
    image = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image", "parent"]
        
    def get_image_url(self, obj):
        return f"{HOST_URL}{obj.image.url}"
