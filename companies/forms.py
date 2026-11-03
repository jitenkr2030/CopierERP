from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["code", "name", "legal_name", "category", "contact_person",
                  "designation", "phone", "alt_phone", "email", "website",
                  "address_line1", "address_line2", "city", "state", "pincode",
                  "country", "gstin", "pan", "credit_limit", "payment_terms_days",
                  "opening_balance", "opening_balance_type", "is_active"]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "legal_name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "contact_person": forms.TextInput(attrs={"class": "form-control"}),
            "designation": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "alt_phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "address_line1": forms.TextInput(attrs={"class": "form-control"}),
            "address_line2": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "pincode": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "gstin": forms.TextInput(attrs={"class": "form-control"}),
            "pan": forms.TextInput(attrs={"class": "form-control"}),
            "credit_limit": forms.NumberInput(attrs={"class": "form-control"}),
            "payment_terms_days": forms.NumberInput(attrs={"class": "form-control"}),
            "opening_balance": forms.NumberInput(attrs={"class": "form-control"}),
            "opening_balance_type": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
