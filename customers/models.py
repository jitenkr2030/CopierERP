from django.db import models
from companies.models import Company


class Customer(models.Model):
    """Customer-specific extension of Company."""
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="customer_profile")
    customer_since = models.DateField(null=True, blank=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    default_discount_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["company__name"]

    def __str__(self):
        return self.company.name

    @property
    def name(self):
        return self.company.name
