from django.db import models
from django.conf import settings


class Notification(models.Model):
    NOTIF_TYPES = [
        ("low_stock", "Low Stock"),
        ("pending_purchase_approval", "Pending Purchase Approval"),
        ("pending_requirement", "Pending Requirement"),
        ("follow_up_reminder", "Follow-up Reminder"),
        ("customer_payment_due", "Customer Payment Due"),
        ("supplier_payment_due", "Supplier Payment Due"),
        ("overdue_invoice", "Overdue Invoice"),
        ("daily_summary", "Daily Summary"),
        ("task", "Task"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="notifications", null=True, blank=True)
    notif_type = models.CharField(max_length=40, choices=NOTIF_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.created_at:%Y-%m-%d %H:%M})"
