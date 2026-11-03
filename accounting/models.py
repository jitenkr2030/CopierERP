from django.db import models
from django.conf import settings


class EntityConfig(models.Model):
    """Bridge record: maps our ERP business entity to a django_ledger Entity."""
    entity_id = models.UUIDField(unique=True)
    name = models.CharField(max_length=200, default="Copier Business ERP")
    is_default = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AccountingEntryMap(models.Model):
    """Map a business transaction (Purchase / Sale / Payment / Receipt)
    to a django_ledger JournalEntry so we can display reversals & history.
    """
    source_model = models.CharField(max_length=60)            # "Purchase", "Sale", ...
    source_pk = models.PositiveIntegerField()
    journal_entry_id = models.UUIDField(null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_reversed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-posted_at"]
        unique_together = ("source_model", "source_pk")

    def __str__(self):
        return f"{self.source_model}/{self.source_pk}"
