from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

# Create your models here.

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    """Category Model"""
    name = models.CharField(max_length=255, verbose_name="имя")
    description = models.TextField(verbose_name="описание")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    """Product Model"""
    name = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    image_preview = models.ImageField(upload_to="products/", verbose_name="изображение", **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата изменения")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="владелец", **NULLABLE)

    def __str__(self):
        return f"{self.name}, {self.description}, {self.price}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"


class Version(models.Model):
    """Version Model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='versions', verbose_name="продукт")
    number = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="номер")
    name = models.CharField(max_length=255, verbose_name="название")
    is_active = models.BooleanField(default=False, verbose_name="активность")

    def __str__(self):
        return f"{self.number}, {self.name}, {self.is_active}"

    class Meta:
        verbose_name = "версия"
        verbose_name_plural = "версии"
        unique_together = ("product", "number")
