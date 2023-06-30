from config import HOST_URL
from news.models import News
from rest_framework import serializers


class NewsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = News
        fields = "__all__"

    def get_image_url(self, obj):
        return f"{HOST_URL}{obj.image.url}"
