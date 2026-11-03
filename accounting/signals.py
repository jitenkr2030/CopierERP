"""
Auto-wires business transactions into django_ledger journal entries.

Each "posted" purchase / confirmed sale / recorded payment or receipt
automatically calls accounting.services.post_*_journal().
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _safe(fn, instance, user=None):
    try:
        return fn(instance, user=user)
    except Exception as exc:
        logger.warning("Accounting hook skipped: %s", exc)


@receiver(post_save, sender="purchases.Purchase")
def _purchase_posted(sender, instance, created, **kw):
    if instance.status == "approved":
        from .services import post_purchase_journal
        _safe(post_purchase_journal, instance, user=instance.approved_by)


@receiver(post_save, sender="sales.Sale")
def _sale_posted(sender, instance, created, **kw):
    if instance.status in ("confirmed", "invoiced", "delivered"):
        from .services import post_sale_journal
        _safe(post_sale_journal, instance, user=instance.created_by)


@receiver(post_save, sender="payments.Payment")
def _payment_posted(sender, instance, created, **kw):
    if created:
        from .services import post_payment_journal
        _safe(post_payment_journal, instance, user=instance.user)


@receiver(post_save, sender="payments.Receipt")
def _receipt_posted(sender, instance, created, **kw):
    if created:
        from .services import post_receipt_journal
        _safe(post_receipt_journal, instance, user=instance.user)


@receiver(post_save, sender="expenses.Expense")
def _expense_posted(sender, instance, created, **kw):
    if created:
        from .services import post_expense_journal
        _safe(post_expense_journal, instance, user=instance.user)
