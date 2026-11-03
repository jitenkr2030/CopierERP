from django.urls import path
from . import views

app_name = "gst"

urlpatterns = [
    path("", views.GSTDashboardView.as_view(), name="dashboard"),
    path("settings/", views.GSTSettingsView.as_view(), name="settings"),
    path("rates/", views.GSTRateListView.as_view(), name="rate_list"),
    path("rates/new/", views.GSTRateCreateView.as_view(), name="rate_create"),
    path("hsn/", views.HSNCodeListView.as_view(), name="hsn_list"),
    path("hsn/new/", views.HSNCodeCreateView.as_view(), name="hsn_create"),
    path("reports/gstr-1/", views.GSTR1ReportView.as_view(), name="gstr1"),
    path("reports/gstr-3b/", views.GSTR3BReportView.as_view(), name="gstr3b"),
]
