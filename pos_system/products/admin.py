from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")

class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =("name", "price", "stock", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("name",)

    inlines = [ImageInline]