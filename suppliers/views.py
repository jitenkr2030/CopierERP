from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Supplier
from .forms import SupplierForm


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = "suppliers/supplier_list.html"
    paginate_by = 25
    context_object_name = "suppliers"

    def get_queryset(self):
        qs = Supplier.objects.select_related("company")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(company__name__icontains=q) | qs.filter(company__code__icontains=q)
        return qs

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "suppliers"
        return ctx


class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "suppliers/supplier_form.html"
    success_url = reverse_lazy("suppliers:supplier_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "suppliers"
        ctx["title"] = "Add Supplier"
        return ctx


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "suppliers/supplier_form.html"
    success_url = reverse_lazy("suppliers:supplier_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "suppliers"
        ctx["title"] = "Edit Supplier"
        return ctx


class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = "suppliers/supplier_detail.html"
    context_object_name = "supplier"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "suppliers"
        return ctx
