from django_filters import rest_framework as filters
from rest_framework import generics, parsers

from .models import Product, ProductExternalId, ProductImage
from .serializers import ImageSerializer, ProductExternalIdSerializer, ProductSerializer
from rest_framework.permissions import IsAdminUser
from django.db.models import Q
from rest_framework import viewsets


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


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = ProductSerializer
    filterset_class = ProductListFilter
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()


class SingleProduct(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()


class PopularProducts(generics.ListAPIView):
    queryset = Product.objects.filter(is_popular=True)
    serializer_class = ProductSerializer


class ExternalIdRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductExternalId.objects.all()
    serializer_class = ProductExternalIdSerializer
    permission_classes = [IsAdminUser]


class ExternalIdCreateApiView(generics.CreateAPIView):
    queryset = ProductExternalId.objects.all()
    serializer_class = ProductExternalIdSerializer
    permission_classes = [IsAdminUser]


class ProductImageCrateApiView(generics.CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(image=self.request.data.get("image"))


class ProductImageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [parsers.MultiPartParser]

    def perform_update(self, serializer):
        image_file = self.request.data.get("image", None)

        if image_file:
            serializer.validated_data["image"] = image_file
            serializer.save()
        else:
            serializer.save()
