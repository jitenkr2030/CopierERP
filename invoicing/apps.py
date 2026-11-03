from django.apps import AppConfig


class InvoicingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "invoicing"
    label = "invoicing"
    verbose_name = "Invoicing"
