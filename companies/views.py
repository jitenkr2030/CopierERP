from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Company
from .forms import CompanyForm


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = "companies/company_list.html"
    paginate_by = 25
    context_object_name = "companies"

    def get_queryset(self):
        qs = Company.objects.select_related()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(code__icontains=q) | qs.filter(gstin__icontains=q)
        cat = self.request.GET.get("category")
        if cat:
            qs = qs.filter(category=cat)
        return qs

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "companies"
        return ctx


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "companies/company_form.html"
    success_url = reverse_lazy("companies:company_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "companies"
        ctx["title"] = "Add Company"
        return ctx


class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "companies/company_form.html"
    success_url = reverse_lazy("companies:company_list")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "companies"
        ctx["title"] = "Edit Company"
        return ctx


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = "companies/company_detail.html"
    context_object_name = "company"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "companies"
        c = self.object
        # show recent purchases, sales, issues, calls, requirements
        try:
            from purchases.models import Purchase
            ctx["purchases"] = Purchase.objects.filter(supplier=c).order_by("-id")[:10]
        except Exception:
            ctx["purchases"] = []
        try:
            from sales.models import Sale
            ctx["sales"] = Sale.objects.filter(customer=c).order_by("-id")[:10]
        except Exception:
            ctx["sales"] = []
        try:
            from stock_issues.models import StockIssue
            ctx["issues"] = StockIssue.objects.filter(company=c).order_by("-id")[:10]
        except Exception:
            ctx["issues"] = []
        try:
            from crm.models import Call
            ctx["calls"] = Call.objects.filter(company=c).order_by("-id")[:10]
        except Exception:
            ctx["calls"] = []
        return ctx
