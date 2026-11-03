from django.db import models
from django.conf import settings
from companies.models import Company
from products.models import Product
from stock_issues.models import StockIssue


class StockReturn(models.Model):
    RETURN_TYPE = [
        ("issue_return", "Issue Return"),
        ("damaged_return", "Damaged Return"),
        ("partial_return", "Partial Return"),
    ]
    return_number = models.CharField(max_length=40, unique=True)
    issue = models.ForeignKey(StockIssue, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name="returns")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="stock_returns")
    return_date = models.DateField()
    return_type = models.CharField(max_length=20, choices=RETURN_TYPE, default="issue_return")
    remarks = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-return_date", "-id"]

    def __str__(self):
        return f"{self.return_number} - {self.company}"


class StockReturnItem(models.Model):
    stock_return = models.ForeignKey(StockReturn, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remarks = models.CharField(max_length=255, blank=True)

    @property
    def line_total(self):
        return self.quantity * self.rate
