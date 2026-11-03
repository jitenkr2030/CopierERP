from django.urls import path
from . import views

app_name = "accounting"

urlpatterns = [
    path("", views.AccountingDashboardView.as_view(), name="dashboard"),
    path("setup/", views.SetupLedgerView.as_view(), name="setup_ledger"),
    path("entries/", views.EntryMapListView.as_view(), name="entry_map_list"),
]
