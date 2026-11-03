from django.contrib import admin
from .models import StockIssue, StockIssueItem


class StockIssueItemInline(admin.TabularInline):
    model = StockIssueItem
    extra = 1


@admin.register(StockIssue)
class StockIssueAdmin(admin.ModelAdmin):
    list_display = ("issue_number", "company", "issue_date", "purpose", "approval_status")
    list_filter = ("purpose", "approval_status")
    search_fields = ("issue_number", "company__name", "reference_number")
    inlines = [StockIssueItemInline]
