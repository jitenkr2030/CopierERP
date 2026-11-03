from django.contrib import admin
from .models import Requirement, RequirementItem


class RequirementItemInline(admin.TabularInline):
    model = RequirementItem
    extra = 1


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ("requirement_number", "company", "requirement_date",
                    "priority", "status", "assigned_to")
    list_filter = ("priority", "status")
    search_fields = ("requirement_number", "company__name")
    inlines = [RequirementItemInline]
