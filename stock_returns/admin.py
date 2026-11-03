from django.contrib import admin
from .models import StockReturn, StockReturnItem


class StockReturnItemInline(admin.TabularInline):
    model = StockReturnItem
    extra = 1


@admin.register(StockReturn)
class StockReturnAdmin(admin.ModelAdmin):
    list_display = ("return_number", "company", "return_date", "return_type")
    list_filter = ("return_type",)
    search_fields = ("return_number", "company__name")
    inlines = [StockReturnItemInline]
