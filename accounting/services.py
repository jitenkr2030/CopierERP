"""
Accounting integration layer.

Wires business transactions (purchase, sale, payment, receipt) into
Django Ledger journal entries.  Implemented defensively: if django_ledger
is not configured yet, calls simply log a warning and return None.
"""
import logging
from decimal import Decimal
from datetime import date
from django.utils import timezone

logger = logging.getLogger(__name__)


def _get_entity():
    from .models import EntityConfig
    cfg = EntityConfig.objects.filter(is_default=True).first()
    if not cfg:
        return None
    try:
        from django_ledger.models.entity import EntityModel
        return EntityModel.objects.get(uuid=cfg.entity_id)
    except Exception as exc:
        logger.warning("django_ledger entity %s not available: %s", cfg.entity_id, exc)
        return None


def _get_or_create_ledger(entity):
    """Get or create the default general-ledger for an entity."""
    from django_ledger.models.ledger import LedgerModel
    ledger, _ = LedgerModel.objects.get_or_create(
        entity=entity, name="General Ledger",
        defaults={"ledger_xid": "gl-main"},
    )
    return ledger


def _account_by_code(entity, code):
    """Look up a django_ledger account by its code in the entity's CoA."""
    from django_ledger.models.accounts import AccountModel
    return AccountModel.objects.filter(coa_model__entity=entity, code=code).first()


def _make_je(entity, ledger, description, user=None):
    """Create a draft JournalEntryModel. Caller is responsible for transactions."""
    from django_ledger.models.journal_entry import JournalEntryModel
    je = JournalEntryModel.objects.create(
        ledger=ledger,
        description=description,
        timestamp=timezone.now(),
        posted=False,
    )
    return je


def _post_txn(je, account, tx_type, amount, description=""):
    """Create a TransactionModel row. Returns None on missing account."""
    if not account or not amount:
        return None
    from django_ledger.models.transactions import TransactionModel
    return TransactionModel.objects.create(
        journal_entry=je, account=account, tx_type=tx_type,
        amount=Decimal(amount), description=description,
    )


def _mark_posted(je):
    je.posted = True
    je.save(update_fields=["posted"])


def post_purchase_journal(purchase, user=None):
    """Dr Inventory, Cr Supplier Payable."""
    entity = _get_entity()
    if not entity:
        return None
    try:
        from .models import AccountingEntryMap
        ledger = _get_or_create_ledger(entity)
        je = _make_je(entity, ledger, f"Purchase {purchase.purchase_number}", user)
        inv = _account_by_code(entity, "1300")   # Inventory
        ap = _account_by_code(entity, "2100")    # Accounts Payable
        amt = Decimal(purchase.total_amount or 0)
        _post_txn(je, inv, "debit", amt)
        _post_txn(je, ap,  "credit", amt)
        _mark_posted(je)
        return AccountingEntryMap.objects.create(
            source_model="Purchase", source_pk=purchase.pk,
            journal_entry_id=je.uuid, posted_by=user,
        )
    except Exception as exc:
        logger.exception("post_purchase_journal failed: %s", exc)
        return None


def post_sale_journal(sale, user=None):
    """Dr Customer Receivable, Cr Sales + Cr Output GST."""
    entity = _get_entity()
    if not entity:
        return None
    try:
        from .models import AccountingEntryMap
        ledger = _get_or_create_ledger(entity)
        je = _make_je(entity, ledger, f"Sale {sale.sale_number}", user)
        ar = _account_by_code(entity, "1200")    # AR
        sales = _account_by_code(entity, "4000")  # Sales Income
        gst = _account_by_code(entity, "2200")   # GST Payable
        total = Decimal(sale.total_amount or 0)
        gst_amt = (Decimal(sale.igst_amount or 0)
                   + Decimal(sale.cgst_amount or 0)
                   + Decimal(sale.sgst_amount or 0))
        taxable = total - gst_amt
        _post_txn(je, ar,    "debit",  total)
        _post_txn(je, sales, "credit", taxable)
        if gst_amt:
            _post_txn(je, gst, "credit", gst_amt)
        _mark_posted(je)
        return AccountingEntryMap.objects.create(
            source_model="Sale", source_pk=sale.pk,
            journal_entry_id=je.uuid, posted_by=user,
        )
    except Exception as exc:
        logger.exception("post_sale_journal failed: %s", exc)
        return None


def post_payment_journal(payment, user=None):
    """Dr Supplier Payable, Cr Bank/Cash."""
    entity = _get_entity()
    if not entity:
        return None
    try:
        from .models import AccountingEntryMap
        ledger = _get_or_create_ledger(entity)
        je = _make_je(entity, ledger, f"Payment {payment.payment_number}", user)
        ap = _account_by_code(entity, "2100")
        cash = _account_by_code(entity, "1010")
        amt = Decimal(payment.amount or 0)
        _post_txn(je, ap,   "debit",  amt)
        _post_txn(je, cash, "credit", amt)
        _mark_posted(je)
        return AccountingEntryMap.objects.create(
            source_model="Payment", source_pk=payment.pk,
            journal_entry_id=je.uuid, posted_by=user,
        )
    except Exception as exc:
        logger.exception("post_payment_journal failed: %s", exc)
        return None


def post_receipt_journal(receipt, user=None):
    """Dr Bank, Cr Customer Receivable."""
    entity = _get_entity()
    if not entity:
        return None
    try:
        from .models import AccountingEntryMap
        ledger = _get_or_create_ledger(entity)
        je = _make_je(entity, ledger, f"Receipt {receipt.receipt_number}", user)
        ar = _account_by_code(entity, "1200")
        cash = _account_by_code(entity, "1010")
        amt = Decimal(receipt.amount or 0)
        _post_txn(je, cash, "debit",  amt)
        _post_txn(je, ar,   "credit", amt)
        _mark_posted(je)
        return AccountingEntryMap.objects.create(
            source_model="Receipt", source_pk=receipt.pk,
            journal_entry_id=je.uuid, posted_by=user,
        )
    except Exception as exc:
        logger.exception("post_receipt_journal failed: %s", exc)
        return None


def post_expense_journal(expense, user=None):
    """Dr Expense, Cr Cash."""
    entity = _get_entity()
    if not entity:
        return None
    try:
        from .models import AccountingEntryMap
        ledger = _get_or_create_ledger(entity)
        je = _make_je(entity, ledger, f"Expense {expense.expense_number}", user)
        exp = _account_by_code(entity, "6000")
        cash = _account_by_code(entity, "1010")
        amt = Decimal(expense.amount or 0)
        _post_txn(je, exp,  "debit",  amt)
        _post_txn(je, cash, "credit", amt)
        _mark_posted(je)
        return AccountingEntryMap.objects.create(
            source_model="Expense", source_pk=expense.pk,
            journal_entry_id=je.uuid, posted_by=user,
        )
    except Exception as exc:
        logger.exception("post_expense_journal failed: %s", exc)
        return None
