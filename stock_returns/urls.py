from django.urls import path
from . import views

app_name = "stock_returns"

urlpatterns = [
    path("", views.StockReturnListView.as_view(), name="return_list"),
    path("new/", views.StockReturnCreateView.as_view(), name="return_create"),
    path("<int:pk>/", views.StockReturnDetailView.as_view(), name="return_detail"),
    path("<int:pk>/edit/", views.StockReturnUpdateView.as_view(), name="return_edit"),
]
