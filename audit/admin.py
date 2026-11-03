from django.contrib import admin
from .models import AuditLog, TransactionLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "action", "model_name", "object_repr")
    list_filter = ("action", "model_name")
    search_fields = ("object_repr", "description", "user__username")
    readonly_fields = ("created_at", "user", "action", "model_name", "object_id",
                       "object_repr", "description", "changes", "ip_address")


@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "transaction_type", "transaction_number", "action")
    search_fields = ("transaction_number", "transaction_type")
    readonly_fields = ("created_at",)
