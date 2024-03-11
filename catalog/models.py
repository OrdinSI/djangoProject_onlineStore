from django.db import models

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

    def __str__(self):
        return (f"{self.name}, {self.description}, {self.price}, {self.category}")

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
