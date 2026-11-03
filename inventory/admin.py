from django.contrib import admin
from .models import Location, StockLedger, StockAdjustment, StockTransfer


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    search_fields = ("code", "name")


@admin.register(StockLedger)
class StockLedgerAdmin(admin.ModelAdmin):
    list_display = ("date", "product", "transaction_type", "transaction_id",
                    "quantity_in", "quantity_out", "balance_after", "user")
    list_filter = ("transaction_type", "date")
    search_fields = ("product__name", "transaction_id")
    readonly_fields = ("balance_after", "created_at")


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ("date", "product", "current_qty", "counted_qty", "difference", "reason")
    list_filter = ("reason",)


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ("date", "product", "from_location", "to_location", "quantity")
