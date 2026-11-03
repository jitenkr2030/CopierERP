from django.db import models
from django.conf import settings


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    METHODS = [("cash", "Cash"), ("bank", "Bank"), ("upi", "UPI"),
               ("cheque", "Cheque"), ("neft", "NEFT/RTGS")]
    expense_number = models.CharField(max_length=40, unique=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT,
                                 related_name="expenses")
    expense_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=METHODS, default="cash")
    reference = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    attachment = models.FileField(upload_to="expenses/", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-expense_date", "-id"]

    def __str__(self):
        return f"{self.expense_number} - {self.amount}"


class Income(models.Model):
    income_number = models.CharField(max_length=40, unique=True)
    source = models.CharField(max_length=120)
    income_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-income_date", "-id"]

    def __str__(self):
        return f"{self.income_number} - {self.amount}"
