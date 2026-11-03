from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("", views.SaleListView.as_view(), name="sale_list"),
    path("new/", views.SaleCreateView.as_view(), name="sale_create"),
    path("<int:pk>/", views.SaleDetailView.as_view(), name="sale_detail"),
    path("<int:pk>/edit/", views.SaleUpdateView.as_view(), name="sale_edit"),
    path("<int:pk>/confirm/", views.SaleConfirmView.as_view(), name="sale_confirm"),
    path("<int:pk>/invoice/", views.SaleInvoicePDFView.as_view(), name="sale_invoice"),
]
