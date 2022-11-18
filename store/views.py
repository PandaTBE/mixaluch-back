from rest_framework import generics, status
from rest_framework.response import Response

from categories.models import Category
from django.http import Http404, HttpResponse

from .models import Product
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category = self.request.GET.get("category", None)
        if category is not None:
            available_categories = []
            try:
                current_category = Category.objects.get(slug=category)
                available_categories.append(current_category)
                if current_category.parent is None:
                    child_categories = Category.objects.filter(parent=current_category.id)
                    for category in child_categories:
                        available_categories.append(category)
            except:
                raise Http404("Страница не найдена")
            return Product.objects.filter(category__in=available_categories)

        else:
            return Product.objects.all()


class SingleProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PopularProducts(generics.ListAPIView):
    queryset = Product.objects.filter(is_popular=True)
    serializer_class = ProductSerializer
