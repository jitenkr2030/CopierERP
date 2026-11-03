from django.contrib import admin
from .models import GSTRate, HSNCode, GSTSettings


@admin.register(GSTRate)
class GSTRateAdmin(admin.ModelAdmin):
    list_display = ("rate", "description", "is_active")


@admin.register(HSNCode)
class HSNCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "gst_rate", "is_active")
    search_fields = ("code", "description")


@admin.register(GSTSettings)
class GSTSettingsAdmin(admin.ModelAdmin):
    list_display = ("business_name", "gstin", "state", "state_code")
