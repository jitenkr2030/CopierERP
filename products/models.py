from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=40, unique=True)
    short = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.short


class Product(models.Model):
    code = models.CharField("Product ID", max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products", null=True, blank=True)
    model_no = models.CharField(max_length=80, blank=True)
    sku = models.CharField(max_length=40, unique=True)
    barcode = models.CharField(max_length=80, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name="products")

    purchase_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sales_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mrp = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    minimum_stock = models.PositiveIntegerField(default=10)
    current_stock = models.PositiveIntegerField(default=0)
    reorder_qty = models.PositiveIntegerField(default=0)

    hsn_code = models.CharField(max_length=15, blank=True)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18)
    is_gst_applicable = models.BooleanField(default=True)

    image = models.ImageField(upload_to="products/", null=True, blank=True)
    specifications = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock

    @property
    def stock_value(self):
        return self.current_stock * self.purchase_rate

    def adjust_stock(self, qty, op="+"):
        if op == "+":
            self.current_stock = (self.current_stock or 0) + qty
        else:
            self.current_stock = max(0, (self.current_stock or 0) - qty)
        self.save(update_fields=["current_stock", "updated_at"])
