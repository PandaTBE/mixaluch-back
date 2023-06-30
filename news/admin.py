from django.contrib import admin
from news.models import News

# Register your models here.


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
