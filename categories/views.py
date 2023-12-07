import genericpath
from rest_framework import generics

from .models import Category
from .serializers import CategorySerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MainCategoriesListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_main=True)
    serializer_class = CategorySerializer
