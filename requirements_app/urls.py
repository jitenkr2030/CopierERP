from django.urls import path
from . import views

app_name = "requirements_app"

urlpatterns = [
    path("", views.RequirementListView.as_view(), name="requirement_list"),
    path("new/", views.RequirementCreateView.as_view(), name="requirement_create"),
    path("<int:pk>/", views.RequirementDetailView.as_view(), name="requirement_detail"),
    path("<int:pk>/edit/", views.RequirementUpdateView.as_view(), name="requirement_edit"),
    path("<int:pk>/check-stock/", views.RequirementCheckStockView.as_view(),
         name="requirement_check_stock"),
]
