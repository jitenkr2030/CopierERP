from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404

from .models import Product, Category, Brand, Unit
from .forms import ProductForm, CategoryForm, BrandForm, UnitForm


# ---- Products ----
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products/product_list.html"
    paginate_by = 25
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.select_related("category", "brand", "unit")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(code__icontains=q)
                | Q(sku__icontains=q) | Q(barcode__icontains=q)
                | Q(model_no__icontains=q)
            )
        cat = self.request.GET.get("category")
        if cat:
            qs = qs.filter(category_id=cat)
        low = self.request.GET.get("low_stock")
        if low:
            from django.db.models import F
            qs = qs.filter(current_stock__lte=F("minimum_stock"))
        return qs

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "products"
        ctx["categories"] = Category.objects.filter(is_active=True)
        return ctx


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:product_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "products"
        ctx["title"] = "Add Product"
        return ctx


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:product_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "products"
        ctx["title"] = "Edit Product"
        return ctx


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "products"
        # recent stock history
        try:
            from inventory.models import StockLedger
            ctx["stock_history"] = StockLedger.objects.filter(product=self.object).order_by("-id")[:10]
        except Exception:
            ctx["stock_history"] = []
        return ctx


# ---- Categories ----
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "products/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "products"
        return ctx


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("products:category_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "products"
        return ctx


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("products:category_list")


# ---- Brands ----
class BrandListView(LoginRequiredMixin, ListView):
    model = Brand
    template_name = "products/brand_list.html"
    context_object_name = "brands"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "products"
        return ctx


class BrandCreateView(LoginRequiredMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = "products/brand_form.html"
    success_url = reverse_lazy("products:brand_list")


class BrandUpdateView(LoginRequiredMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "products/brand_form.html"
    success_url = reverse_lazy("products:brand_list")


# ---- Units ----
class UnitListView(LoginRequiredMixin, ListView):
    model = Unit
    template_name = "products/unit_list.html"
    context_object_name = "units"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "products"
        return ctx


class UnitCreateView(LoginRequiredMixin, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = "products/unit_form.html"
    success_url = reverse_lazy("products:unit_list")


class UnitUpdateView(LoginRequiredMixin, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = "products/unit_form.html"
    success_url = reverse_lazy("products:unit_list")
