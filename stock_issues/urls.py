from django.urls import path
from . import views

app_name = "stock_issues"

urlpatterns = [
    path("", views.StockIssueListView.as_view(), name="issue_list"),
    path("new/", views.StockIssueCreateView.as_view(), name="issue_create"),
    path("<int:pk>/", views.StockIssueDetailView.as_view(), name="issue_detail"),
    path("<int:pk>/edit/", views.StockIssueUpdateView.as_view(), name="issue_edit"),
    path("<int:pk>/approve/", views.StockIssueApproveView.as_view(), name="issue_approve"),
]
