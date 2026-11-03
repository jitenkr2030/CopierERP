from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.utils import timezone

from .models import Purchase, PurchaseItem
from .forms import PurchaseForm, PurchaseItemFormSet
from inventory.models import StockLedger
from audit.utils import log_action


class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "purchases/purchase_list.html"
    paginate_by = 25
    context_object_name = "purchases"

    def get_queryset(self):
        qs = Purchase.objects.select_related("supplier")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(purchase_number__icontains=q) | qs.filter(supplier__name__icontains=q)
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs.order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "purchases"
        ctx["statuses"] = Purchase.STATUS_CHOICES
        return ctx


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchase_form.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "purchases"
        ctx["title"] = "Create Purchase"
        if self.request.POST:
            ctx["items"] = PurchaseItemFormSet(self.request.POST)
        else:
            ctx["items"] = PurchaseItemFormSet()
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
        log_action(self.request.user, "create", "Purchase",
                   self.object.id, str(self.object), "Purchase created", request=self.request)
        return redirect("purchases:purchase_detail", pk=self.object.pk)


class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchase_form.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "purchases"
        ctx["title"] = "Edit Purchase"
        if self.request.POST:
            ctx["items"] = PurchaseItemFormSet(self.request.POST, instance=self.object)
        else:
            ctx["items"] = PurchaseItemFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        items = ctx["items"]
        with transaction.atomic():
            self.object = form.save()
            if items.is_valid():
                items.save()
            self.object.recalc()
        log_action(self.request.user, "update", "Purchase",
                   self.object.id, str(self.object), "Purchase updated", request=self.request)
        return redirect("purchases:purchase_detail", pk=self.object.pk)


class PurchaseDetailView(LoginRequiredMixin, DetailView):
    model = Purchase
    template_name = "purchases/purchase_detail.html"
    context_object_name = "purchase"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "purchases"
        return ctx


class PurchaseApproveView(LoginRequiredMixin, View):
    def get(self, request, pk):
        p = get_object_or_404(Purchase, pk=pk)
        if p.status != "approved":
            p.status = "approved"
            p.approved_by = request.user
            p.save(update_fields=["status", "approved_by"])
            # Post stock
            for it in p.items.all():
                StockLedger.append_entry(
                    date=p.purchase_date, product=it.product,
                    transaction_type="purchase",
                    transaction_id=p.purchase_number,
                    transaction_model="Purchase", ref_pk=p.id,
                    quantity_in=it.quantity, company=p.supplier,
                    location=p.location, rate=it.rate,
                    remarks=f"Purchase {p.purchase_number}", user=request.user,
                )
            log_action(request.user, "approve", "Purchase", p.id, str(p),
                       "Purchase approved & stock posted", request=request)
        return redirect("purchases:purchase_detail", pk=p.pk)


class PurchaseCancelView(LoginRequiredMixin, View):
    def get(self, request, pk):
        p = get_object_or_404(Purchase, pk=pk)
        if p.status == "approved":
            # Reverse stock
            for it in p.items.all():
                StockLedger.append_entry(
                    date=timezone.localdate(), product=it.product,
                    transaction_type="purchase_return",
                    transaction_id=f"REV-{p.purchase_number}",
                    transaction_model="Purchase", ref_pk=p.id,
                    quantity_out=it.quantity, company=p.supplier,
                    location=p.location, rate=it.rate,
                    remarks=f"Reversal of {p.purchase_number}", user=request.user,
                )
            p.status = "cancelled"
            p.save(update_fields=["status"])
            log_action(request.user, "cancel", "Purchase", p.id, str(p),
                       "Purchase cancelled & reversed", request=request)
        return redirect("purchases:purchase_detail", pk=p.pk)
