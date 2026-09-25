from django_filters import rest_framework as filters
from rest_framework import generics, parsers
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .models import Product, ProductExternalId, ProductImage
from .serializers import ImageSerializer, ProductCardSerializer, ProductExternalIdSerializer, ProductSerializer
from rest_framework.permissions import IsAdminUser
from django.db.models import Q
from rest_framework import viewsets
from categories.models import Category


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


class ProductListV2Pagination(PageNumberPagination):
    page_size = 24


class ProductListV2View(generics.ListAPIView):
    serializer_class = ProductCardSerializer
    pagination_class = ProductListV2Pagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        params = self.request.query_params
        category_value = params.get("category")
        search = params.get("search", "").strip()
        sort_by = params.get("sort_by", "price")
        sort_order = params.get("sort_order", "desc")
        if len(search) > 255:
            raise ValidationError({"search": "Не более 255 символов."})
        if sort_by not in ("price", "name"):
            raise ValidationError({"sort_by": "Допустимые значения: price, name."})
        if sort_order not in ("asc", "desc"):
            raise ValidationError({"sort_order": "Допустимые значения: asc, desc."})

        queryset = Product.objects.filter(is_active=True, category__is_active=True)
        hidden_branches = Q()
        for tree_id, left, right in Category.objects.filter(is_active=False).values_list(
            "tree_id", "lft", "rght"
        ):
            hidden_branches |= Q(
                category__tree_id=tree_id,
                category__lft__gte=left,
                category__rght__lte=right,
            )
        if hidden_branches:
            queryset = queryset.exclude(hidden_branches)

        if category_value is not None:
            if not category_value.isascii() or not category_value.isdecimal() or len(category_value) > 19:
                raise ValidationError({"category": "Укажите числовой ID категории."})
            category_id = int(category_value)
            if category_id < 1 or category_id > 2**63 - 1:
                raise ValidationError({"category": "Укажите числовой ID категории."})
            category = Category.objects.filter(pk=category_id, is_active=True).first()
            if category is None or Category.objects.filter(
                tree_id=category.tree_id, lft__lte=category.lft,
                rght__gte=category.rght, is_active=False,
            ).exists():
                raise ValidationError({"category": "Категория не найдена или скрыта."})
            queryset = queryset.filter(category__in=category.get_descendants(include_self=True))

        if search:
            matching_categories = Q(pk__in=[])
            for tree_id, left, right in Category.objects.filter(
                name__icontains=search
            ).values_list("tree_id", "lft", "rght"):
                matching_categories |= Q(
                    category__tree_id=tree_id,
                    category__lft__gte=left,
                    category__rght__lte=right,
                )
            queryset = queryset.filter(Q(title__icontains=search) | matching_categories)
        ordering = {
            "price": "regular_price",
            "name": "title",
        }[sort_by]
        if sort_order == "desc":
            ordering = f"-{ordering}"
        return queryset.prefetch_related("product_image").order_by(ordering, "-id")


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
