from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "customer", "invoice_date", "invoice_type",
                    "total_amount", "paid_amount", "is_paid")
    list_filter = ("invoice_type", "is_paid")
    search_fields = ("invoice_number", "customer__name")
