from django.db import models
from companies.models import Company


class Supplier(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="supplier_profile")
    supplier_since = models.DateField(null=True, blank=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_terms_days = models.PositiveIntegerField(default=30)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["company__name"]

    def __str__(self):
        return self.company.name

    @property
    def name(self):
        return self.company.name
