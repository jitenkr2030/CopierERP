from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, LoginHistory


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "employee_id", "role",
                    "is_active_employee", "is_staff", "is_superuser")
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email", "employee_id", "first_name", "last_name")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Employee Info", {"fields": ("employee_id", "phone", "role",
                                       "is_active_employee", "date_joined_company",
                                       "avatar")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Employee Info", {"fields": ("employee_id", "phone", "role",
                                       "is_active_employee", "avatar")}),
    )


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "login_time", "logout_time", "ip_address", "was_successful")
    list_filter = ("was_successful",)
    search_fields = ("user__username", "ip_address")
    readonly_fields = ("login_time", "ip_address", "user_agent")
