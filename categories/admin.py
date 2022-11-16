from mptt.admin import MPTTModelAdmin

from django.contrib import admin

from .models import Category

admin.site.register(Category, MPTTModelAdmin)
