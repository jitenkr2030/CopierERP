from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db import transaction

from .models import StockIssue, StockIssueItem
from .forms import StockIssueForm, StockIssueItemFormSet
from inventory.models import StockLedger
from audit.utils import log_action


class StockIssueListView(LoginRequiredMixin, ListView):
    model = StockIssue
    template_name = "stock_issues/issue_list.html"
    paginate_by = 25
    context_object_name = "issues"

    def get_queryset(self):
        qs = StockIssue.objects.select_related("company", "employee")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(approval_status=status)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(issue_number__icontains=q) | qs.filter(company__name__icontains=q)
        return qs.order_by("-id")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "stock_issues"
        ctx["statuses"] = StockIssue.APPROVAL_STATUS
        return ctx


class StockIssueCreateView(LoginRequiredMixin, CreateView):
    model = StockIssue
    form_class = StockIssueForm
    template_name = "stock_issues/issue_form.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "stock_issues"
        ctx["title"] = "Create Stock Issue"
        if self.request.POST:
            ctx["items"] = StockIssueItemFormSet(self.request.POST)
        else:
            ctx["items"] = StockIssueItemFormSet()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        items = ctx["items"]
        with transaction.atomic():
            form.instance.issued_by = self.request.user
            self.object = form.save()
            items.instance = self.object
            if items.is_valid():
                items.save()
        log_action(self.request.user, "create", "StockIssue",
                   self.object.id, str(self.object), "Stock issue created",
                   request=self.request)
        return redirect("stock_issues:issue_detail", pk=self.object.pk)


class StockIssueUpdateView(LoginRequiredMixin, UpdateView):
    model = StockIssue
    form_class = StockIssueForm
    template_name = "stock_issues/issue_form.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "stock_issues"
        ctx["title"] = "Edit Stock Issue"
        if self.request.POST:
            ctx["items"] = StockIssueItemFormSet(self.request.POST, instance=self.object)
        else:
            ctx["items"] = StockIssueItemFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        items = ctx["items"]
        with transaction.atomic():
            self.object = form.save()
            if items.is_valid():
                items.save()
        return redirect("stock_issues:issue_detail", pk=self.object.pk)


class StockIssueDetailView(LoginRequiredMixin, DetailView):
    model = StockIssue
    template_name = "stock_issues/issue_detail.html"
    context_object_name = "issue"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "stock_issues"
        return ctx


class StockIssueApproveView(LoginRequiredMixin, View):
    def get(self, request, pk):
        si = get_object_or_404(StockIssue, pk=pk)
        if si.approval_status == "pending":
            si.approval_status = "approved"
            si.approved_by = request.user
            si.save(update_fields=["approval_status", "approved_by"])
            for it in si.items.all():
                StockLedger.append_entry(
                    date=si.issue_date, product=it.product,
                    transaction_type="stock_issue",
                    transaction_id=si.issue_number,
                    transaction_model="StockIssue", ref_pk=si.id,
                    quantity_out=it.quantity, company=si.company,
                    location=si.location, rate=it.rate,
                    remarks=f"Issue {si.issue_number}", user=request.user,
                )
            log_action(request.user, "approve", "StockIssue", si.id, str(si),
                       "Stock issue approved & posted", request=request)
        return redirect("stock_issues:issue_detail", pk=si.pk)
