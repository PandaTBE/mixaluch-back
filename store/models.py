from tabnanny import verbose

from categories.models import Category
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ProductType(models.Model):
    """
    В таблице типов продуктов будет представлен список различных
    типов продуктов, которые продаются.
    """

    name = models.CharField(verbose_name=_("Product name"),
                            help_text=_("Required"),
                            max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product type")
        verbose_name_plural = _("Product types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    Таблица спецификаций продукта содержит спецификации
    или характеристики для типа продукта.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"),
                            help_text=_("Required"),
                            max_length=255)

    class Meta:
        verbose_name = _("Product specification")
        verbose_name_plural = _("Product specifications")

    def __str__(self):
        return self.name


class ProductUnit(models.TextChoices):
    KG = "KG", "кг"
    PC = "PC", "шт"


PRODUCT_UNIT_MAP = {"KG": "кг", "PC": "шт"}


class Product(models.Model):
    """
    таблица продуктов содержит все продукты
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("Title"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(verbose_name=_("Description"),
                                   help_text=_("Not Required"),
                                   blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.IntegerField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 9999"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 9999."),
            },
        },
    )
    discount_price = models.IntegerField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 9999"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 9999."),
            },
        },
    )
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    is_popular = models.BooleanField(verbose_name=_("Is popular?"),
                                     default=False)
    created_at = models.DateTimeField(_("Created at"),
                                      auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    unit = models.CharField(max_length=50,
                            choices=ProductUnit.choices,
                            default=ProductUnit.KG)
    min_quantity = models.FloatField(default=0.3,
                                     verbose_name=_("Min quantity"))

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    """
    Таблица значений спецификации продукта содержит
    Индивидуальную спецификацию продуктов или индивидуальные особенности.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification,
                                      on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("Value"),
        help_text=_("Product specification value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    таблица изображения
    """

    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="product_image")
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload a product image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
