from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db import transaction

from .models import StockReturn, StockReturnItem
from .forms import StockReturnForm, StockReturnItemFormSet
from inventory.models import StockLedger
from audit.utils import log_action


class StockReturnListView(LoginRequiredMixin, ListView):
    model = StockReturn
    template_name = "stock_returns/return_list.html"
    paginate_by = 25
    context_object_name = "returns"

    def get_queryset(self):
        return StockReturn.objects.select_related("company", "issue").order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "stock_returns"
        return ctx


class StockReturnCreateView(LoginRequiredMixin, CreateView):
    model = StockReturn
    form_class = StockReturnForm
    template_name = "stock_returns/return_form.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "stock_returns"
        ctx["title"] = "Create Stock Return"
        if self.request.POST:
            ctx["items"] = StockReturnItemFormSet(self.request.POST)
        else:
            ctx["items"] = StockReturnItemFormSet()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        items = ctx["items"]
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            items.instance = self.object
            if items.is_valid():
                items.save()
            # Post stock back in
            for it in self.object.items.all():
                StockLedger.append_entry(
                    date=self.object.return_date, product=it.product,
                    transaction_type="stock_return",
                    transaction_id=self.object.return_number,
                    transaction_model="StockReturn", ref_pk=self.object.id,
                    quantity_in=it.quantity, company=self.object.company,
                    rate=it.rate,
                    remarks=f"Return {self.object.return_number}", user=self.request.user,
                )
        log_action(self.request.user, "create", "StockReturn",
                   self.object.id, str(self.object), "Stock return created",
                   request=self.request)
        return redirect("stock_returns:return_detail", pk=self.object.pk)


class StockReturnDetailView(LoginRequiredMixin, DetailView):
    model = StockReturn
    template_name = "stock_returns/return_detail.html"
    context_object_name = "stock_return"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "stock_returns"
        return ctx


class StockReturnUpdateView(LoginRequiredMixin, UpdateView):
    model = StockReturn
    form_class = StockReturnForm
    template_name = "stock_returns/return_form.html"
    success_url = reverse_lazy("stock_returns:return_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "stock_returns"
        ctx["title"] = "Edit Stock Return"
        if self.request.POST:
            ctx["items"] = StockReturnItemFormSet(self.request.POST, instance=self.object)
        else:
            ctx["items"] = StockReturnItemFormSet(instance=self.object)
        return ctx
