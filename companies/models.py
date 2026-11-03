from django.db import models
from django.utils import timezone


class CompanyCategory(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    SUPPLIER = "supplier", "Supplier"
    BOTH = "both", "Customer & Supplier"
    OTHER = "other", "Other"


class Company(models.Model):
    """A registered business entity (customer / supplier / both)."""
    code = models.CharField("Company ID", max_length=20, unique=True)
    name = models.CharField(max_length=200)
    legal_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CompanyCategory.choices, default=CompanyCategory.OTHER)

    # contact info
    contact_person = models.CharField(max_length=120, blank=True)
    designation = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    alt_phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    # address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=80, blank=True)
    state = models.CharField(max_length=80, blank=True)
    pincode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=60, default="India")

    # tax & commercial
    gstin = models.CharField("GSTIN", max_length=20, blank=True)
    pan = models.CharField(max_length=20, blank=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_terms_days = models.PositiveIntegerField(default=30)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    opening_balance_type = models.CharField(max_length=10, choices=[("dr", "Debit"), ("cr", "Credit")], default="dr")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def outstanding_balance(self):
        """Computed from ledgers — placeholder = 0 if ledgers missing."""
        try:
            from payments.models import Payment, Receipt
        except Exception:
            return 0
        return 0
