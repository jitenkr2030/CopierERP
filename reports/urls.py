from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.ReportsIndexView.as_view(), name="index"),
    path("stock-statement/", views.StockStatementView.as_view(), name="stock_statement"),
    path("purchase-register/", views.PurchaseRegisterView.as_view(), name="purchase_register"),
    path("sales-register/", views.SalesRegisterView.as_view(), name="sales_register"),
    path("outstanding/", views.OutstandingReportView.as_view(), name="outstanding"),
    path("low-stock/", views.LowStockReportView.as_view(), name="low_stock"),
]
