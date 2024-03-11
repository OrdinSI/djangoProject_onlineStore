from django.contrib import admin

from catalog.models import Product, Category, Version


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'description')
    search_fields = ('name', 'description',)
    list_filter = ('category',)


@admin.register(Version)
class Version(admin.ModelAdmin):
    list_display = ('id', 'product', 'number', 'name', 'is_active')
    list_filter = ('product',)
