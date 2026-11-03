from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = [
    ("super_admin", "Super Admin"),
    ("administrator", "Administrator"),
    ("manager", "Manager"),
    ("accountant", "Accountant"),
    ("store_manager", "Store Manager"),
    ("employee", "Employee"),
    ("viewer", "Viewer"),
]

ROLE_PERMISSIONS = {
    "super_admin":   ["*"],
    "administrator": ["companies", "products", "purchases", "inventory",
                      "sales", "invoices", "crm", "requirements", "payments",
                      "gst", "expenses", "reports", "imports_exports"],
    "manager":       ["companies", "products", "purchases", "inventory",
                      "sales", "invoices", "crm", "requirements", "reports"],
    "accountant":    ["payments", "accounting", "gst", "expenses", "reports"],
    "store_manager": ["products", "purchases", "inventory", "stock_issues",
                      "stock_returns", "imports_exports"],
    "employee":      ["crm", "requirements"],
    "viewer":        [],
}


class User(AbstractUser):
    """Custom user with employee metadata and role."""
    ROLE_CHOICES = ROLE_CHOICES

    employee_id = models.CharField("Employee ID", max_length=20, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    is_active_employee = models.BooleanField(default=True)
    date_joined_company = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    REQUIRED_FIELDS = ["email", "role"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]

    def __str__(self):
        name = self.get_full_name() or self.username
        return f"{name} ({self.get_role_display()})"

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    def has_module_access(self, module_key):
        if self.is_superuser or self.role == "super_admin":
            return True
        perms = ROLE_PERMISSIONS.get(self.role, [])
        return "*" in perms or module_key in perms


class LoginHistory(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="logins")
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    was_successful = models.BooleanField(default=True)

    class Meta:
        ordering = ["-login_time"]

    def __str__(self):
        return f"{self.user.username} @ {self.login_time:%Y-%m-%d %H:%M}"
