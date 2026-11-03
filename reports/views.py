from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.db.models import Sum, F
from datetime import date


class ReportsIndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "reports/index.html", {"segment": "reports"})


class StockStatementView(LoginRequiredMixin, View):
    def get(self, request):
        from products.models import Product
        from inventory.models import StockLedger
        date_from = request.GET.get("from")
        date_to = request.GET.get("to")
        ledger = StockLedger.objects.select_related("product")
        if date_from:
            ledger = ledger.filter(date__gte=date_from)
        if date_to:
            ledger = ledger.filter(date__lte=date_to)
        agg = ledger.values("product__code", "product__name").annotate(
            opening=Sum("quantity_in") - Sum("quantity_out"),
            purchased=Sum("quantity_in"),
            issued=Sum("quantity_out"),
        ).order_by("product__code")
        return render(request, "reports/stock_statement.html", {
            "segment": "reports",
            "rows": agg,
            "from": date_from, "to": date_to,
        })


class PurchaseRegisterView(LoginRequiredMixin, View):
    def get(self, request):
        from purchases.models import Purchase
        date_from = request.GET.get("from")
        date_to = request.GET.get("to")
        qs = Purchase.objects.select_related("supplier")
        if date_from:
            qs = qs.filter(purchase_date__gte=date_from)
        if date_to:
            qs = qs.filter(purchase_date__lte=date_to)
        return render(request, "reports/purchase_register.html", {
            "segment": "reports", "rows": qs.order_by("-id"),
            "from": date_from, "to": date_to,
            "total": qs.aggregate(t=Sum("total_amount"))["t"] or 0,
        })


class SalesRegisterView(LoginRequiredMixin, View):
    def get(self, request):
        from sales.models import Sale
        date_from = request.GET.get("from")
        date_to = request.GET.get("to")
        qs = Sale.objects.select_related("customer")
        if date_from:
            qs = qs.filter(sale_date__gte=date_from)
        if date_to:
            qs = qs.filter(sale_date__lte=date_to)
        return render(request, "reports/sales_register.html", {
            "segment": "reports", "rows": qs.order_by("-id"),
            "from": date_from, "to": date_to,
            "total": qs.aggregate(t=Sum("total_amount"))["t"] or 0,
        })


class OutstandingReportView(LoginRequiredMixin, View):
    def get(self, request):
        from companies.models import Company
        from purchases.models import Purchase
        from sales.models import Sale
        suppliers = []
        for c in Company.objects.filter(category__in=["supplier", "both"]):
            tot = Purchase.objects.filter(supplier=c).aggregate(t=Sum("total_amount"))["t"] or 0
            paid = Purchase.objects.filter(supplier=c).aggregate(t=Sum("paid_amount"))["t"] or 0
            if tot - paid > 0:
                suppliers.append({"company": c, "balance": tot - paid})
        customers = []
        for c in Company.objects.filter(category__in=["customer", "both"]):
            tot = Sale.objects.filter(customer=c).aggregate(t=Sum("total_amount"))["t"] or 0
            customers.append({"company": c, "balance": tot})
        return render(request, "reports/outstanding.html", {
            "segment": "reports", "suppliers": suppliers, "customers": customers,
        })


class LowStockReportView(LoginRequiredMixin, View):
    def get(self, request):
        from products.models import Product
        rows = Product.objects.filter(current_stock__lte=F("minimum_stock"))
        return render(request, "reports/low_stock.html",
                      {"segment": "reports", "rows": rows})
