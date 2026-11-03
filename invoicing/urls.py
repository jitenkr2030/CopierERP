from django.urls import path
from . import views

app_name = "invoicing"

urlpatterns = [
    path("", views.InvoiceListView.as_view(), name="invoice_list"),
    path("new/", views.InvoiceCreateView.as_view(), name="invoice_create"),
    path("<int:pk>/", views.InvoiceDetailView.as_view(), name="invoice_detail"),
    path("<int:pk>/edit/", views.InvoiceUpdateView.as_view(), name="invoice_edit"),
]
