from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("company", "customer_since", "credit_limit", "default_discount_pct")
    search_fields = ("company__name",)
    autocomplete_fields = ("company",)
