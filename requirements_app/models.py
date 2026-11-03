from django.db import models
from django.conf import settings
from companies.models import Company
from products.models import Product


class Requirement(models.Model):
    PRIORITY = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]
    STATUS = [
        ("new", "New"),
        ("pending_stock_check", "Pending Stock Check"),
        ("available", "Available"),
        ("unavailable", "Unavailable"),
        ("converted_purchase", "Converted to Purchase"),
        ("converted_sale", "Converted to Sale"),
        ("converted_issue", "Converted to Stock Issue"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    requirement_number = models.CharField(max_length=40, unique=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="requirements")
    requirement_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY, default="medium")
    expected_delivery_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name="requirements_assigned")
    status = models.CharField(max_length=30, choices=STATUS, default="new")
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  null=True, related_name="requirements_created")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-requirement_date", "-id"]
        verbose_name = "Requirement"
        verbose_name_plural = "Requirements"

    def __str__(self):
        return f"{self.requirement_number} - {self.company}"


class RequirementItem(models.Model):
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    required_qty = models.PositiveIntegerField(default=1)
    fulfilled_qty = models.PositiveIntegerField(default=0)

    @property
    def pending_qty(self):
        return max(0, self.required_qty - self.fulfilled_qty)

    def __str__(self):
        return f"{self.product} x {self.required_qty} (pending {self.pending_qty})"
