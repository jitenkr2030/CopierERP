from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("company", "supplier_since", "credit_limit", "payment_terms_days")
    search_fields = ("company__name",)
    autocomplete_fields = ("company",)
