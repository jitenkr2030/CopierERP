from django.db import models
from django.conf import settings
from companies.models import Company
from products.models import Product
from inventory.models import Location
from accounts.models import User


class StockIssue(models.Model):
    PURPOSE_CHOICES = [
        ("sale", "Sale"),
        ("transfer", "Transfer"),
        ("sample", "Sample"),
        ("internal_consumption", "Internal Consumption"),
        ("other", "Other"),
    ]
    APPROVAL_STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    issue_number = models.CharField(max_length=40, unique=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="stock_issues")
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="stock_issues_issued")
    issue_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    purpose = models.CharField(max_length=30, choices=PURPOSE_CHOICES, default="other")
    reference_number = models.CharField(max_length=80, blank=True)
    remarks = models.TextField(blank=True)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default="pending")

    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                 related_name="issues_made")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name="issues_approved")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-issue_date", "-id"]

    def __str__(self):
        return f"{self.issue_number} - {self.company}"


class StockIssueItem(models.Model):
    issue = models.ForeignKey(StockIssue, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remarks = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def line_total(self):
        return self.quantity * self.rate
