from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.db.models import Sum
from .models import Location, StockLedger, StockAdjustment, StockTransfer
from .forms import LocationForm, StockAdjustmentForm, StockTransferForm


class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = "inventory/location_list.html"
    context_object_name = "locations"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "inventory"
        return ctx


class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = "inventory/location_form.html"
    success_url = reverse_lazy("inventory:location_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "inventory"
        return ctx


class StockLedgerListView(LoginRequiredMixin, ListView):
    model = StockLedger
    template_name = "inventory/stock_ledger_list.html"
    paginate_by = 50
    context_object_name = "ledger"

    def get_queryset(self):
        qs = StockLedger.objects.select_related("product", "company", "user")
        pid = self.request.GET.get("product")
        if pid:
            qs = qs.filter(product_id=pid)
        ttype = self.request.GET.get("type")
        if ttype:
            qs = qs.filter(transaction_type=ttype)
        date_from = self.request.GET.get("from")
        date_to = self.request.GET.get("to")
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        return qs.order_by("-date", "-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "inventory"
        ctx["types"] = StockLedger.TRANSACTION_TYPES
        from products.models import Product
        ctx["products"] = Product.objects.all().order_by("name")
        return ctx


class StockAdjustmentListView(LoginRequiredMixin, ListView):
    model = StockAdjustment
    template_name = "inventory/adjustment_list.html"
    paginate_by = 30
    context_object_name = "adjustments"

    def get_queryset(self):
        return StockAdjustment.objects.select_related("product").order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "inventory"
        return ctx


class StockAdjustmentCreateView(LoginRequiredMixin, CreateView):
    model = StockAdjustment
    form_class = StockAdjustmentForm
    template_name = "inventory/adjustment_form.html"
    success_url = reverse_lazy("inventory:adjustment_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "inventory"
        return ctx


class StockTransferListView(LoginRequiredMixin, ListView):
    model = StockTransfer
    template_name = "inventory/transfer_list.html"
    paginate_by = 30
    context_object_name = "transfers"

    def get_queryset(self):
        return StockTransfer.objects.select_related("product", "from_location", "to_location").order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "inventory"
        return ctx


class StockTransferCreateView(LoginRequiredMixin, CreateView):
    model = StockTransfer
    form_class = StockTransferForm
    template_name = "inventory/transfer_form.html"
    success_url = reverse_lazy("inventory:transfer_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "inventory"
        return ctx
