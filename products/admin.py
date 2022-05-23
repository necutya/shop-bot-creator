from django.contrib import admin
from .models import Category, Product, ProductPhoto


@admin.register(Category)
class Category(admin.ModelAdmin):
    pass


@admin.register(Product)
class Product(admin.ModelAdmin):
    pass


@admin.register(ProductPhoto)
class ProductPhoto(admin.ModelAdmin):
    pass
