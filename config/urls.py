"""Root URL configuration for Copier Business ERP."""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (
    LoginView, LogoutView, dashboard,
    UserListView, UserCreateView, UserUpdateView, UserDetailView,
    RoleListView, ProfileView, LoginHistoryView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # auth
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # dashboard
    path("", dashboard, name="dashboard"),

    # users & access
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/new/", UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("roles/", RoleListView.as_view(), name="role_list"),
    path("login-history/", LoginHistoryView.as_view(), name="login_history"),

    # business modules
    path("companies/", include("companies.urls")),
    path("customers/", include("customers.urls")),
    path("suppliers/", include("suppliers.urls")),
    path("products/", include("products.urls")),
    path("purchases/", include("purchases.urls")),
    path("inventory/", include("inventory.urls")),
    path("stock-issues/", include("stock_issues.urls")),
    path("stock-returns/", include("stock_returns.urls")),
    path("sales/", include("sales.urls")),
    path("invoices/", include("invoicing.urls")),
    path("calls/", include("crm.urls")),
    path("requirements/", include("requirements_app.urls")),
    path("payments/", include("payments.urls")),
    path("accounting/", include("accounting.urls")),
    path("gst/", include("gst.urls")),
    path("expenses/", include("expenses.urls")),
    path("reports/", include("reports.urls")),
    path("import-export/", include("imports_exports.urls")),
    path("notifications/", include("notifications.urls")),
    path("audit/", include("audit.urls")),

    # django-ledger native views (chart of accounts, journals, reports)
    path("ledger/", include("django_ledger.urls", namespace="django_ledger")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler for 403/404/500 -> simple templates
handler404 = "accounts.views.handler404"
handler500 = "accounts.views.handler500"
