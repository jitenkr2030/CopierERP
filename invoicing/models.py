from django.db import models
from django.conf import settings
from companies.models import Company
from sales.models import Sale


class Invoice(models.Model):
    INVOICE_TYPES = [
        ("tax_invoice", "Tax Invoice"),
        ("credit_note", "Credit Note"),
        ("debit_note", "Debit Note"),
        ("delivery_challan", "Delivery Challan"),
    ]
    invoice_number = models.CharField(max_length=40, unique=True)
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES, default="tax_invoice")
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="invoices")
    customer = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="invoices")
    invoice_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-invoice_date", "-id"]

    def __str__(self):
        return f"{self.invoice_number} - {self.customer}"

    @property
    def balance_due(self):
        return max(0, self.total_amount - self.paid_amount)
