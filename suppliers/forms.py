from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["company", "supplier_since", "credit_limit", "payment_terms_days", "notes"]
        widgets = {
            "company": forms.Select(attrs={"class": "form-select"}),
            "supplier_since": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "credit_limit": forms.NumberInput(attrs={"class": "form-control"}),
            "payment_terms_days": forms.NumberInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
