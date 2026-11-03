from django.db import models


class GSTRate(models.Model):
    rate = models.DecimalField(max_digits=5, decimal_places=2, unique=True)
    description = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["rate"]

    def __str__(self):
        return f"{self.rate}%"


class HSNCode(models.Model):
    code = models.CharField(max_length=15, unique=True)
    description = models.CharField(max_length=200, blank=True)
    gst_rate = models.ForeignKey(GSTRate, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.description[:40]}"


class GSTSettings(models.Model):
    """One row — company GST registration details."""
    business_name = models.CharField(max_length=200)
    gstin = models.CharField(max_length=20)
    state = models.CharField(max_length=80)
    state_code = models.CharField(max_length=4)
    is_interstate = models.BooleanField(default=False)
    financial_year_start = models.DateField()

    def __str__(self):
        return f"{self.business_name} - {self.gstin}"
