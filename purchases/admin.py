from django.contrib import admin
from .models import Purchase, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("purchase_number", "supplier", "purchase_date", "total_amount",
                    "payment_status", "status")
    list_filter = ("status", "payment_status", "payment_method")
    search_fields = ("purchase_number", "supplier_invoice_no", "supplier__name")
    inlines = [PurchaseItemInline]
    readonly_fields = ("subtotal", "cgst_amount", "sgst_amount", "igst_amount", "total_amount",
                       "created_at", "updated_at", "approved_by")


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ("purchase", "product", "quantity", "rate", "gst_rate", "line_total")
