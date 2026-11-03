from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Payment, Receipt, BankAccount
from .forms import PaymentForm, ReceiptForm, BankAccountForm


# ---- Payments ----
class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = "payments/payment_list.html"
    paginate_by = 25
    context_object_name = "payments"

    def get_queryset(self):
        return Payment.objects.select_related("supplier", "purchase").order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "payments"
        return ctx


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payments/payment_form.html"
    success_url = reverse_lazy("payments:payment_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "payments"
        ctx["title"] = "Record Payment"
        return ctx


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payments/payment_form.html"
    success_url = reverse_lazy("payments:payment_list")


class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = "payments/payment_detail.html"
    context_object_name = "payment"


# ---- Receipts ----
class ReceiptListView(LoginRequiredMixin, ListView):
    model = Receipt
    template_name = "payments/receipt_list.html"
    paginate_by = 25
    context_object_name = "receipts"

    def get_queryset(self):
        return Receipt.objects.select_related("customer", "sale").order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "payments"
        return ctx


class ReceiptCreateView(LoginRequiredMixin, CreateView):
    model = Receipt
    form_class = ReceiptForm
    template_name = "payments/receipt_form.html"
    success_url = reverse_lazy("payments:receipt_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "payments"
        ctx["title"] = "Record Receipt"
        return ctx


class ReceiptUpdateView(LoginRequiredMixin, UpdateView):
    model = Receipt
    form_class = ReceiptForm
    template_name = "payments/receipt_form.html"
    success_url = reverse_lazy("payments:receipt_list")


class ReceiptDetailView(LoginRequiredMixin, DetailView):
    model = Receipt
    template_name = "payments/receipt_detail.html"
    context_object_name = "receipt"


# ---- Bank Accounts ----
class BankAccountListView(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = "payments/bank_account_list.html"
    context_object_name = "accounts"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "payments"
        return ctx


class BankAccountCreateView(LoginRequiredMixin, CreateView):
    model = BankAccount
    form_class = BankAccountForm
    template_name = "payments/bank_account_form.html"
    success_url = reverse_lazy("payments:bank_account_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "payments"
        return ctx


class BankAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = BankAccount
    form_class = BankAccountForm
    template_name = "payments/bank_account_form.html"
    success_url = reverse_lazy("payments:bank_account_list")
