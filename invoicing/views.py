from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Invoice
from .forms import InvoiceForm


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = "invoicing/invoice_list.html"
    paginate_by = 25
    context_object_name = "invoices"

    def get_queryset(self):
        qs = Invoice.objects.select_related("customer", "sale")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(invoice_number__icontains=q) | qs.filter(customer__name__icontains=q)
        return qs.order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "invoices"
        return ctx


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoicing/invoice_form.html"
    success_url = reverse_lazy("invoicing:invoice_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "invoices"
        ctx["title"] = "Create Invoice"
        return ctx


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "invoicing/invoice_form.html"
    success_url = reverse_lazy("invoicing:invoice_list")


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = "invoicing/invoice_detail.html"
    context_object_name = "invoice"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "invoices"
        return ctx
