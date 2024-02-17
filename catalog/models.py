from django.db import models

# Create your models here.

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    """Category Model"""
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Description")

    def __str__(self):
        return f"{self.name}, {self.description}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    """Product Model"""
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    image_preview = models.ImageField(upload_to="products/", verbose_name="Preview image", **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date added")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date modified")
    manufactured_at = models.DateTimeField(auto_now_add=True, verbose_name="Manufactured")

    def __str__(self):
        return (f"{self.name}, {self.description}, "
                f"{self.price}, {self.created_at}, {self.updated_at}, {self.category}")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
