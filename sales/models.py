from django.db import models
from django.conf import settings
from companies.models import Company
from products.models import Product
from inventory.models import Location


class Sale(models.Model):
    SALE_TYPES = [
        ("quotation", "Quotation"),
        ("order", "Sales Order"),
        ("invoice", "Tax Invoice"),
        ("delivery_challan", "Delivery Challan"),
        ("cash_sale", "Cash Sale"),
        ("credit_sale", "Credit Sale"),
    ]
    STATUS = [
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("invoiced", "Invoiced"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    sale_number = models.CharField(max_length=40, unique=True)
    sale_type = models.CharField(max_length=20, choices=SALE_TYPES, default="invoice")
    customer = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="sales",
                                 limit_choices_to={"category__in": ["customer", "both"]})
    sale_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    billing_address = models.TextField(blank=True)
    shipping_address = models.TextField(blank=True)
    customer_gstin = models.CharField(max_length=20, blank=True)

    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    igst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    round_off = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS, default="draft")
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name="sales_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-sale_date", "-id"]

    def __str__(self):
        return f"{self.sale_number} - {self.customer}"

    @property
    def total_paid(self):
        from payments.models import Receipt
        return Receipt.objects.filter(sale=self).aggregate(t=models.Sum("amount"))["t"] or 0

    @property
    def balance_due(self):
        return max(0, self.total_amount - self.total_paid)

    def recalc(self):
        items = self.items.all()
        sub = sum(i.line_total for i in items)
        self.subtotal = sub
        taxable = sub - self.discount_amount
        total_gst = sum(i.gst_amount for i in items)
        self.igst_amount = total_gst
        self.cgst_amount = 0
        self.sgst_amount = 0
        self.total_amount = taxable + total_gst + self.round_off
        self.save()


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=20, default="Piece")
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18)
    hsn_code = models.CharField(max_length=15, blank=True)

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
