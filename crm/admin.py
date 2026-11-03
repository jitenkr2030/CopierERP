from django.contrib import admin
from .models import Call, FollowUp


class FollowUpInline(admin.TabularInline):
    model = FollowUp
    extra = 0


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ("call_id", "company", "contact_person", "call_date",
                    "direction", "status", "assigned_to")
    list_filter = ("status", "direction")
    search_fields = ("call_id", "company__name", "contact_person", "phone")
    inlines = [FollowUpInline]
    autocomplete_fields = ("company",)


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ("call", "date", "next_follow_up", "done_by")
