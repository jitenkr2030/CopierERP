from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.db.models import Sum, Q

from .models import GSTRate, HSNCode, GSTSettings
from .forms import GSTRateForm, HSNCodeForm, GSTSettingsForm


class GSTDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "gst/dashboard.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "gst"
        ctx["settings"] = GSTSettings.objects.first()
        ctx["rates"] = GSTRate.objects.filter(is_active=True)
        ctx["hsn_count"] = HSNCode.objects.count()
        # Quick purchase / sales GST totals
        from purchases.models import Purchase
        from sales.models import Sale
        today = __import__("datetime").date.today()
        month_start = today.replace(day=1)
        ctx["purchase_gst"] = Purchase.objects.filter(purchase_date__gte=month_start).aggregate(
            t=Sum("igst_amount") + Sum("cgst_amount") + Sum("sgst_amount"))["t"] or 0
        ctx["sales_gst"] = Sale.objects.filter(sale_date__gte=month_start).aggregate(
            t=Sum("igst_amount") + Sum("cgst_amount") + Sum("sgst_amount"))["t"] or 0
        return ctx


class GSTRateListView(LoginRequiredMixin, ListView):
    model = GSTRate
    template_name = "gst/rate_list.html"
    context_object_name = "rates"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "gst"
        return ctx


class GSTRateCreateView(LoginRequiredMixin, CreateView):
    model = GSTRate
    form_class = GSTRateForm
    template_name = "gst/rate_form.html"
    success_url = reverse_lazy("gst:rate_list")


class HSNCodeListView(LoginRequiredMixin, ListView):
    model = HSNCode
    template_name = "gst/hsn_list.html"
    context_object_name = "hsns"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "gst"
        return ctx


class HSNCodeCreateView(LoginRequiredMixin, CreateView):
    model = HSNCode
    form_class = HSNCodeForm
    template_name = "gst/hsn_form.html"
    success_url = reverse_lazy("gst:hsn_list")


class GSTSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        instance = GSTSettings.objects.first()
        form = GSTSettingsForm(instance=instance)
        return render(request, "gst/settings_form.html", {"form": form, "segment": "gst"})

    def post(self, request):
        instance = GSTSettings.objects.first()
        form = GSTSettingsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("gst:dashboard")
        return render(request, "gst/settings_form.html", {"form": form, "segment": "gst"})


class GSTR1ReportView(LoginRequiredMixin, TemplateView):
    template_name = "gst/gstr1.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "gst"
        from sales.models import Sale
        ctx["sales"] = Sale.objects.select_related("customer").order_by("-sale_date")
        return ctx


class GSTR3BReportView(LoginRequiredMixin, TemplateView):
    template_name = "gst/gstr3b.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "gst"
        from sales.models import Sale
        from purchases.models import Purchase
        ctx["sales_total"] = Sale.objects.aggregate(
            t=Sum("subtotal"))["t"] or 0
        ctx["purchase_total"] = Purchase.objects.aggregate(
            t=Sum("subtotal"))["t"] or 0
        ctx["output_gst"] = Sale.objects.aggregate(
            t=Sum("igst_amount") + Sum("cgst_amount") + Sum("sgst_amount"))["t"] or 0
        ctx["input_gst"] = Purchase.objects.aggregate(
            t=Sum("igst_amount") + Sum("cgst_amount") + Sum("sgst_amount"))["t"] or 0
        return ctx
