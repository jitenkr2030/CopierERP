from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView

from .models import EntityConfig, AccountingEntryMap


class AccountingDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounting/dashboard.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "accounting"
        ctx["entity"] = EntityConfig.objects.filter(is_default=True).first()
        ctx["entries"] = AccountingEntryMap.objects.select_related("posted_by")[:50]
        return ctx


class SetupLedgerView(LoginRequiredMixin, View):
    """Create a django_ledger Entity + default CoA once."""
    def get(self, request):
        try:
            from django_ledger.models.entity import EntityModel
            from django_ledger.models.chart_of_accounts import ChartOfAccountModel
            from django_ledger.models.accounts import AccountModel
            from django_ledger.io.roles import (
                ASSET_CA_CASH, ASSET_CA_INVENTORY, ASSET_CA_RECEIVABLES,
                LIABILITY_CL_ACC_PAYABLE, EQUITY_CAPITAL,
                INCOME_OPERATIONAL, EXPENSE_OPERATIONAL, COGS_REGULAR,
            )
            from django_ledger.models.ledger import LedgerModel

            if not EntityConfig.objects.filter(is_default=True).exists():
                # Create entity via treebeard add_root (returns EntityModel)
                entity = EntityModel.objects.add_root(
                    create_kwargs={
                        "name": "Copier Business ERP",
                        "admin_id": request.user.pk,
                        "accrual_method": True,
                        "fy_start_month": 4,
                    },
                )
                # Create CoA
                coa = ChartOfAccountModel.objects.create(
                    entity=entity, name="Default Chart of Accounts",
                )
                # Create the standard set of accounts using django_ledger's role constants
                accounts = [
                    # (code, role, name, balance_type)
                    ("1010", ASSET_CA_CASH,             "Cash in Hand",       "debit"),
                    ("1020", ASSET_CA_CASH,             "Bank Account",       "debit"),
                    ("1200", ASSET_CA_RECEIVABLES,      "Accounts Receivable","debit"),
                    ("1300", ASSET_CA_INVENTORY,        "Inventory",          "debit"),
                    ("2100", LIABILITY_CL_ACC_PAYABLE,  "Accounts Payable",   "credit"),
                    ("2200", LIABILITY_CL_ACC_PAYABLE,  "GST Payable",        "credit"),
                    ("3100", EQUITY_CAPITAL,            "Capital",            "credit"),
                    ("4000", INCOME_OPERATIONAL,        "Sales Income",       "credit"),
                    ("5000", COGS_REGULAR,              "Cost of Goods Sold", "debit"),
                    ("6000", EXPENSE_OPERATIONAL,       "Office Expenses",    "debit"),
                    ("6100", EXPENSE_OPERATIONAL,       "Salaries",           "debit"),
                    ("6200", EXPENSE_OPERATIONAL,       "Rent",               "debit"),
                    ("6300", EXPENSE_OPERATIONAL,       "Utilities",          "debit"),
                    ("6400", EXPENSE_OPERATIONAL,       "Bank Charges",       "debit"),
                ]
                root_qs = coa.get_coa_root_accounts_qs()
                for code, role, name, bal in accounts:
                    coa.create_account(
                        code=code, role=role, name=name,
                        balance_type=bal, active=True,
                        root_account_qs=root_qs,
                    )
                # Default ledger
                LedgerModel.objects.get_or_create(
                    entity=entity, name="General Ledger",
                    defaults={"ledger_xid": "gl-main"},
                )
                EntityConfig.objects.create(
                    entity_id=entity.uuid, name=entity.name, is_default=True,
                )
        except Exception as exc:
            import traceback
            traceback.print_exc()
            return render(request, "accounting/error.html", {"error": str(exc)})
        return redirect("accounting:dashboard")


class EntryMapListView(LoginRequiredMixin, ListView):
    model = AccountingEntryMap
    template_name = "accounting/entry_map_list.html"
    paginate_by = 50
    context_object_name = "entries"

    def get_queryset(self):
        return AccountingEntryMap.objects.select_related("posted_by").order_by("-posted_at")

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["segment"] = "accounting"
        return ctx
