from django.contrib import admin
from .models import Category, Brand, Unit, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "short", "is_active")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "category", "brand", "unit",
                    "purchase_rate", "sales_rate", "current_stock", "minimum_stock", "is_active")
    list_filter = ("category", "brand", "is_active")
    search_fields = ("code", "name", "sku", "barcode", "model_no")
    autocomplete_fields = ("category", "brand", "unit")
    readonly_fields = ("created_at", "updated_at", "current_stock")
