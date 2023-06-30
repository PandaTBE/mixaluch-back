from django.db import models

# Create your models here.


class News(models.Model):
    name = models.CharField(max_length=128)
    short_text = models.CharField(max_length=512, default="")
    is_important = models.BooleanField(default=False)
    markdown_text = models.TextField(default="", null=True, blank=True)
    image = models.ImageField(
        verbose_name=("News image"),
        help_text=("Upload news image"),
        upload_to="images/news/",
        default="images/default.png",
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
