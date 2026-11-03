from django.db import models
from django.conf import settings
from companies.models import Company
from products.models import Product
from inventory.models import Location


class Purchase(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("approved", "Approved"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("bank", "Bank"),
        ("upi", "UPI"),
        ("cheque", "Cheque"),
        ("credit", "Credit"),
        ("neft", "NEFT/RTGS"),
    ]
    PAYMENT_STATUS = [
        ("unpaid", "Unpaid"),
        ("partial", "Partial"),
        ("paid", "Paid"),
    ]

    purchase_number = models.CharField(max_length=40, unique=True)
    supplier = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="purchases",
                                  limit_choices_to={"category__in": ["supplier", "both"]})
    supplier_invoice_no = models.CharField(max_length=80, blank=True)
    purchase_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="credit")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="unpaid")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    igst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    attachment = models.FileField(upload_to="purchases/", null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name="purchases_created")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name="purchases_approved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-purchase_date", "-id"]

    def __str__(self):
        return f"{self.purchase_number} - {self.supplier}"

    @property
    def total_paid(self):
        from payments.models import Payment
        return Payment.objects.filter(purchase=self).aggregate(t=models.Sum("amount"))["t"] or 0

    @property
    def balance_due(self):
        return max(0, self.total_amount - self.total_paid)

    def recalc(self):
        items = self.items.all()
        sub = sum(i.line_total for i in items)
        self.subtotal = sub
        taxable = sub - self.discount_amount
        # GST split: assume purchase is intra-state -> CGST+SGST, else IGST
        # (Determined by supplier state vs own state in real life; here we use IGST if supplier state != our state)
        total_gst = sum(i.gst_amount for i in items)
        self.igst_amount = total_gst   # default IGST; can be split later
        self.cgst_amount = 0
        self.sgst_amount = 0
        self.total_amount = taxable + total_gst
        self.save()


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=20, default="Piece")
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def line_gross(self):
        return self.quantity * self.rate

    @property
    def line_discounted(self):
        return self.line_gross - self.discount

    @property
    def gst_amount(self):
        return round(self.line_discounted * self.gst_rate / 100, 2)

    @property
    def line_total(self):
        return self.line_discounted + self.gst_amount
