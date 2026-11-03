from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemFormSet
from inventory.models import StockLedger
from audit.utils import log_action


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = "sales/sale_list.html"
    paginate_by = 25
    context_object_name = "sales"

    def get_queryset(self):
        qs = Sale.objects.select_related("customer")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(sale_number__icontains=q) | qs.filter(customer__name__icontains=q)
        stype = self.request.GET.get("type")
        if stype:
            qs = qs.filter(sale_type=stype)
        return qs.order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "sales"
        ctx["types"] = Sale.SALE_TYPES
        return ctx


class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sales/sale_form.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "sales"
        ctx["title"] = "Create Sale"
        if self.request.POST:
            ctx["items"] = SaleItemFormSet(self.request.POST)
        else:
            ctx["items"] = SaleItemFormSet()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        items = ctx["items"]
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            items.instance = self.object
            if items.is_valid():
                items.save()
            self.object.recalc()
        log_action(self.request.user, "create", "Sale",
                   self.object.id, str(self.object), "Sale created", request=self.request)
        return redirect("sales:sale_detail", pk=self.object.pk)


class SaleUpdateView(LoginRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = "sales/sale_form.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "sales"
        ctx["title"] = "Edit Sale"
        if self.request.POST:
            ctx["items"] = SaleItemFormSet(self.request.POST, instance=self.object)
        else:
            ctx["items"] = SaleItemFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        items = ctx["items"]
        with transaction.atomic():
            self.object = form.save()
            if items.is_valid():
                items.save()
            self.object.recalc()
        return redirect("sales:sale_detail", pk=self.object.pk)


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = "sales/sale_detail.html"
    context_object_name = "sale"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "sales"
        return ctx


class SaleConfirmView(LoginRequiredMixin, View):
    def get(self, request, pk):
        s = get_object_or_404(Sale, pk=pk)
        if s.status == "draft":
            s.status = "confirmed"
            s.save(update_fields=["status"])
            for it in s.items.all():
                StockLedger.append_entry(
                    date=s.sale_date, product=it.product,
                    transaction_type="sales",
                    transaction_id=s.sale_number,
                    transaction_model="Sale", ref_pk=s.id,
                    quantity_out=it.quantity, company=s.customer,
                    location=s.location, rate=it.rate,
                    remarks=f"Sale {s.sale_number}", user=request.user,
                )
            log_action(request.user, "approve", "Sale", s.id, str(s),
                       "Sale confirmed & stock posted", request=request)
        return redirect("sales:sale_detail", pk=s.pk)


class SaleInvoicePDFView(LoginRequiredMixin, View):
    """Quick HTML invoice; PDF printing via browser print."""
    def get(self, request, pk):
        from weasyprint import HTML  # noqa  -- optional; not used in basic install
        sale = get_object_or_404(Sale, pk=pk)
        html = render_to_string("sales/invoice_print.html", {"sale": sale, "company": None})
        return HttpResponse(html)
