from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("new/", views.ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product_edit"),

    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("categories/new/", views.CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", views.CategoryUpdateView.as_view(), name="category_edit"),

    path("brands/", views.BrandListView.as_view(), name="brand_list"),
    path("brands/new/", views.BrandCreateView.as_view(), name="brand_create"),
    path("brands/<int:pk>/edit/", views.BrandUpdateView.as_view(), name="brand_edit"),

    path("units/", views.UnitListView.as_view(), name="unit_list"),
    path("units/new/", views.UnitCreateView.as_view(), name="unit_create"),
    path("units/<int:pk>/edit/", views.UnitUpdateView.as_view(), name="unit_edit"),
]
