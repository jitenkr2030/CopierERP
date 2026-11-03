from django.urls import path
from . import views

app_name = "purchases"

urlpatterns = [
    path("", views.PurchaseListView.as_view(), name="purchase_list"),
    path("new/", views.PurchaseCreateView.as_view(), name="purchase_create"),
    path("<int:pk>/", views.PurchaseDetailView.as_view(), name="purchase_detail"),
    path("<int:pk>/edit/", views.PurchaseUpdateView.as_view(), name="purchase_edit"),
    path("<int:pk>/approve/", views.PurchaseApproveView.as_view(), name="purchase_approve"),
    path("<int:pk>/cancel/", views.PurchaseCancelView.as_view(), name="purchase_cancel"),
]
