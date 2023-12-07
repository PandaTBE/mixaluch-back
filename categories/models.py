from mptt.models import MPTTModel, TreeForeignKey

from django.db import models


class Category(MPTTModel):
    """
    Категория наследуется от mptt модели, так как будет иметь древовидную структуру
    (Мясо-Свинина) (Птица -Индейка)
    """

    name = models.CharField(
        verbose_name="Название категории",
        help_text="Обязательное и уникальное",
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Уникальный адрес для категории", max_length=255, unique=True
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=True)
    image = models.ImageField(
        verbose_name="Изображении категории",
        help_text="Добавьте изображении категории",
        upload_to="images/categories",
        default="images/default.png",
    )
    is_main = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ["id"]

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
