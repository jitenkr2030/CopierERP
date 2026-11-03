from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Customer
from .forms import CustomerForm


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "customers/customer_list.html"
    paginate_by = 25
    context_object_name = "customers"

    def get_queryset(self):
        qs = Customer.objects.select_related("company")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(company__name__icontains=q) | qs.filter(company__code__icontains=q)
        return qs

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "customers"
        return ctx


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customers:customer_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "customers"
        ctx["title"] = "Add Customer"
        return ctx


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customers:customer_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "customers"
        ctx["title"] = "Edit Customer"
        return ctx


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "customers/customer_detail.html"
    context_object_name = "customer"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "customers"
        return ctx
