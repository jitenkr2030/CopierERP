from django.db import models
from django.conf import settings
from products.models import Product
from companies.models import Company


class Location(models.Model):
    name = models.CharField(max_length=80, unique=True)
    code = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class StockLedger(models.Model):
    TRANSACTION_TYPES = [
        ("opening", "Opening Stock"),
        ("purchase", "Purchase"),
        ("stock_issue", "Stock Issue"),
        ("stock_return", "Stock Return"),
        ("sales", "Sales"),
        ("purchase_return", "Purchase Return"),
        ("damaged", "Damaged"),
        ("lost", "Lost"),
        ("adjustment", "Stock Adjustment"),
        ("transfer_in", "Transfer In"),
        ("transfer_out", "Transfer Out"),
    ]

    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="stock_ledger")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    transaction_id = models.CharField(max_length=40, blank=True)        # ref number
    transaction_model = models.CharField(max_length=60, blank=True)     # eg "Purchase"
    ref_pk = models.PositiveIntegerField(null=True, blank=True)
    quantity_in = models.PositiveIntegerField(default=0)
    quantity_out = models.PositiveIntegerField(default=0)
    balance_after = models.PositiveIntegerField(default=0)
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-id"]
        indexes = [models.Index(fields=["product", "date"]),
                   models.Index(fields=["transaction_type", "date"])]

    def __str__(self):
        return f"{self.date} | {self.product} | {self.transaction_type} | +{self.quantity_in} -{self.quantity_out}"

    @classmethod
    def append_entry(cls, *, date, product, transaction_type, transaction_id="",
                     transaction_model="", ref_pk=None, quantity_in=0, quantity_out=0,
                     company=None, location=None, rate=0, remarks="", user=None):
        """Append a stock ledger row, recomputing balance_after for the product."""
        prev_balance = (cls.objects.filter(product=product)
                        .order_by("-date", "-id").first())
        prev_bal = prev_balance.balance_after if prev_balance else (product.current_stock or 0)
        new_balance = max(0, prev_bal + quantity_in - quantity_out)
        entry = cls.objects.create(
            date=date, product=product, location=location, company=company,
            transaction_type=transaction_type, transaction_id=transaction_id,
            transaction_model=transaction_model, ref_pk=ref_pk,
            quantity_in=quantity_in, quantity_out=quantity_out,
            balance_after=new_balance, rate=rate, remarks=remarks, user=user,
        )
        product.current_stock = new_balance
        product.save(update_fields=["current_stock", "updated_at"])
        return entry


class StockAdjustment(models.Model):
    REASON_CHOICES = [
        ("physical_verification", "Physical Verification"),
        ("damaged", "Damaged"),
        ("lost", "Lost"),
        ("other", "Other"),
    ]
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="adjustments")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    current_qty = models.PositiveIntegerField(default=0)
    counted_qty = models.PositiveIntegerField(default=0)
    difference = models.IntegerField(default=0)
    reason = models.CharField(max_length=40, choices=REASON_CHOICES, default="other")
    remarks = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kw):
        self.current_qty = self.product.current_stock or 0
        self.difference = self.counted_qty - self.current_qty
        super().save(*args, **kw)
        # Apply adjustment via ledger
        if self.difference != 0:
            q_in = max(0, self.difference)
            q_out = max(0, -self.difference)
            StockLedger.append_entry(
                date=self.date, product=self.product,
                transaction_type="adjustment",
                transaction_id=f"ADJ-{self.id or 0}",
                transaction_model="StockAdjustment",
                quantity_in=q_in, quantity_out=q_out,
                location=self.location, rate=self.product.purchase_rate,
                remarks=f"Adjustment: {self.get_reason_display()}", user=self.user,
            )


class StockTransfer(models.Model):
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="transfers")
    from_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="transfers_out")
    to_location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="transfers_in")
    quantity = models.PositiveIntegerField()
    remarks = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kw):
        is_new = self.pk is None
        super().save(*args, **kw)
        if is_new:
            StockLedger.append_entry(
                date=self.date, product=self.product,
                transaction_type="transfer_out",
                transaction_id=f"TR-{self.id}", transaction_model="StockTransfer",
                quantity_out=self.quantity, location=self.from_location,
                remarks=f"Transfer to {self.to_location.code}", user=self.user,
            )
