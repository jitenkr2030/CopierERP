from django.contrib import admin
from .models import ExpenseCategory, Expense, Income


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("expense_number", "category", "expense_date", "amount", "payment_method")
    list_filter = ("category", "payment_method", "expense_date")
    search_fields = ("expense_number", "reference", "description")


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("income_number", "source", "income_date", "amount")
    search_fields = ("income_number", "source", "reference")
