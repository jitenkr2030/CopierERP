from django.urls import path
from . import views

app_name = "inventory"

urlpatterns = [
    path("locations/", views.LocationListView.as_view(), name="location_list"),
    path("locations/new/", views.LocationCreateView.as_view(), name="location_create"),
    path("ledger/", views.StockLedgerListView.as_view(), name="stock_ledger"),
    path("adjustments/", views.StockAdjustmentListView.as_view(), name="adjustment_list"),
    path("adjustments/new/", views.StockAdjustmentCreateView.as_view(), name="adjustment_create"),
    path("transfers/", views.StockTransferListView.as_view(), name="transfer_list"),
    path("transfers/new/", views.StockTransferCreateView.as_view(), name="transfer_create"),
]
