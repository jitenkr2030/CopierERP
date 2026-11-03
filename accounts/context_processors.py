from .models import ROLE_CHOICES


def user_role_context(request):
    """Expose current user role + available modules to templates."""
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {"available_modules": [], "current_role": None}
    role = getattr(user, "role", None)
    if user.is_superuser:
        modules = ["companies", "products", "purchases", "inventory",
                   "stock_issues", "stock_returns", "sales", "invoices",
                   "crm", "requirements", "payments", "accounting", "gst",
                   "expenses", "reports", "imports_exports", "audit",
                   "notifications", "users"]
    else:
        from .models import ROLE_PERMISSIONS
        mods = ROLE_PERMISSIONS.get(role, [])
        modules = mods if "*" not in mods else [
            "companies", "products", "purchases", "inventory",
            "stock_issues", "stock_returns", "sales", "invoices",
            "crm", "requirements", "payments", "accounting", "gst",
            "expenses", "reports", "imports_exports", "audit",
            "notifications", "users",
        ]
    return {
        "current_role": role,
        "available_modules": modules,
        "all_roles": ROLE_CHOICES,
    }
