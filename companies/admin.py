from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "category", "contact_person", "city",
                    "gstin", "is_active")
    list_filter = ("category", "is_active", "city")
    search_fields = ("name", "code", "contact_person", "gstin", "phone", "email")
    readonly_fields = ("created_at", "updated_at")
