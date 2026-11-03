from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["company", "customer_since", "credit_limit", "default_discount_pct", "notes"]
        widgets = {
            "company": forms.Select(attrs={"class": "form-select"}),
            "customer_since": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "credit_limit": forms.NumberInput(attrs={"class": "form-control"}),
            "default_discount_pct": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
