from django.urls import path
from . import views

app_name = "audit"

urlpatterns = [
    path("", views.AuditLogListView.as_view(), name="audit_log_list"),
    path("transactions/", views.TransactionLogListView.as_view(), name="transaction_log_list"),
]
