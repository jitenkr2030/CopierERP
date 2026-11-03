from django.apps import AppConfig


class AccountingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounting"
    label = "accounting"
    verbose_name = "Accounting (Django Ledger)"

    def ready(self):
        from . import signals  # noqa: F401
