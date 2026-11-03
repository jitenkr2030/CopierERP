from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """Generic audit log — every meaningful business action."""
    ACTION_CHOICES = [
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("approve", "Approve"),
        ("cancel", "Cancel"),
        ("reverse", "Reverse"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("view", "View"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                            null=True, related_name="audit_logs")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=40, blank=True)
    object_repr = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["model_name", "object_id"]),
                   models.Index(fields=["user", "created_at"])]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} | {self.user} | {self.action} {self.model_name}"


class TransactionLog(models.Model):
    """Specific audit trail for posted transactions (purchases, sales, payments)."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=40)
    transaction_number = models.CharField(max_length=40)
    action = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_type}/{self.transaction_number} - {self.action}"
