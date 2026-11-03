from django.urls import path
from . import views

app_name = "imports_exports"

urlpatterns = [
    path("", views.ImportExportIndexView.as_view(), name="index"),
    path("export/<str:model>/", views.ExportView.as_view(), name="export"),
    path("template/<str:model>/", views.SampleTemplateView.as_view(), name="template"),
    path("import/companies/", views.ImportCompaniesView.as_view(), name="import_companies"),
    path("import/products/", views.ImportProductsView.as_view(), name="import_products"),
]
