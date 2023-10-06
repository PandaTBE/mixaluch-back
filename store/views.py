from django_filters import rest_framework as filters
from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer
from django.db.models import Q


class NumberArrayFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class ProductListFilter(filters.FilterSet):
    title = filters.CharFilter(method="filter_with_or")
    category = filters.CharFilter(method="filter_with_or")
    id = NumberArrayFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = Product
        fields = ["is_popular"]

    def filter_with_or(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(category__name__icontains=value)
        )


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = ProductSerializer
    filterset_class = ProductListFilter


class SingleProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PopularProducts(generics.ListAPIView):
    queryset = Product.objects.filter(is_popular=True)
    serializer_class = ProductSerializer
