from django.db import models
from django.conf import settings
from companies.models import Company
from purchases.models import Purchase
from sales.models import Sale


class Payment(models.Model):
    """Outbound payment (to supplier)."""
    METHODS = [
        ("cash", "Cash"), ("bank", "Bank"), ("upi", "UPI"),
        ("cheque", "Cheque"), ("neft", "NEFT/RTGS"),
    ]
    payment_number = models.CharField(max_length=40, unique=True)
    supplier = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="payments_made",
                                 limit_choices_to={"category__in": ["supplier", "both"]})
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="payments")
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHODS, default="bank")
    reference = models.CharField(max_length=80, blank=True)
    cheque_no = models.CharField(max_length=40, blank=True)
    cheque_date = models.DateField(null=True, blank=True)
    bank = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-payment_date", "-id"]

    def __str__(self):
        return f"{self.payment_number} - {self.supplier} - {self.amount}"


class Receipt(models.Model):
    """Inbound receipt (from customer)."""
    METHODS = [
        ("cash", "Cash"), ("bank", "Bank"), ("upi", "UPI"),
        ("cheque", "Cheque"), ("neft", "NEFT/RTGS"),
    ]
    receipt_number = models.CharField(max_length=40, unique=True)
    customer = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="receipts_received",
                                  limit_choices_to={"category__in": ["customer", "both"]})
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name="receipts")
    receipt_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHODS, default="bank")
    reference = models.CharField(max_length=80, blank=True)
    cheque_no = models.CharField(max_length=40, blank=True)
    cheque_date = models.DateField(null=True, blank=True)
    bank = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-receipt_date", "-id"]

    def __str__(self):
        return f"{self.receipt_number} - {self.customer} - {self.amount}"


class BankAccount(models.Model):
    name = models.CharField(max_length=120)
    bank_name = models.CharField(max_length=120)
    account_number = models.CharField(max_length=40)
    ifsc = models.CharField(max_length=20, blank=True)
    branch = models.CharField(max_length=120, blank=True)
    opening_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
