from django.contrib import admin
from .models import Payment, Receipt, BankAccount


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("payment_number", "supplier", "purchase", "payment_date", "amount", "method")
    list_filter = ("method", "payment_date")
    search_fields = ("payment_number", "supplier__name", "reference", "cheque_no")


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("receipt_number", "customer", "sale", "receipt_date", "amount", "method")
    list_filter = ("method", "receipt_date")
    search_fields = ("receipt_number", "customer__name", "reference", "cheque_no")


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("name", "bank_name", "account_number", "ifsc", "is_active")
    search_fields = ("name", "bank_name", "account_number")
