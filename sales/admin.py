from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("sale_number", "customer", "sale_date", "sale_type",
                    "total_amount", "status")
    list_filter = ("sale_type", "status")
    search_fields = ("sale_number", "customer__name")
    inlines = [SaleItemInline]
    readonly_fields = ("subtotal", "cgst_amount", "sgst_amount", "igst_amount",
                       "total_amount", "created_at", "updated_at")
