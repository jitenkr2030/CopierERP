from django.contrib import admin
from .models import EntityConfig, AccountingEntryMap


@admin.register(EntityConfig)
class EntityConfigAdmin(admin.ModelAdmin):
    list_display = ("name", "entity_id", "is_default")


@admin.register(AccountingEntryMap)
class AccountingEntryMapAdmin(admin.ModelAdmin):
    list_display = ("source_model", "source_pk", "journal_entry_id",
                    "posted_at", "posted_by", "is_reversed")
    list_filter = ("source_model", "is_reversed")
