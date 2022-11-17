from django.http import HttpResponse, Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.response import  Response

from .models import Product
from .serializers import ProductSerializer
from categories.models import Category


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SingleProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PopularProducts(generics.ListAPIView):
    queryset = Product.objects.filter(is_popular=True)
    serializer_class = ProductSerializer


class ProductsByCategorySlug(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        slug = self.kwargs["slug"]
        available_categories = []
        try:
            current_category = Category.objects.get(slug=slug)
            available_categories.append(current_category)
            if current_category.parent is None:
                child_categories = Category.objects.filter(parent=current_category.id)
                for category in child_categories:
                    available_categories.append(category)
        except:
            raise Http404('Страница не найдена')

        return Product.objects.filter(category__in=available_categories)
