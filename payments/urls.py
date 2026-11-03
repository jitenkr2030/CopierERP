from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("", views.PaymentListView.as_view(), name="payment_list"),
    path("new/", views.PaymentCreateView.as_view(), name="payment_create"),
    path("<int:pk>/", views.PaymentDetailView.as_view(), name="payment_detail"),
    path("<int:pk>/edit/", views.PaymentUpdateView.as_view(), name="payment_edit"),

    path("receipts/", views.ReceiptListView.as_view(), name="receipt_list"),
    path("receipts/new/", views.ReceiptCreateView.as_view(), name="receipt_create"),
    path("receipts/<int:pk>/", views.ReceiptDetailView.as_view(), name="receipt_detail"),
    path("receipts/<int:pk>/edit/", views.ReceiptUpdateView.as_view(), name="receipt_edit"),

    path("bank-accounts/", views.BankAccountListView.as_view(), name="bank_account_list"),
    path("bank-accounts/new/", views.BankAccountCreateView.as_view(), name="bank_account_create"),
    path("bank-accounts/<int:pk>/edit/", views.BankAccountUpdateView.as_view(), name="bank_account_edit"),
]
