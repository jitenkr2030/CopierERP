from django import forms
from .models import GSTRate, HSNCode, GSTSettings


class GSTRateForm(forms.ModelForm):
    class Meta:
        model = GSTRate
        fields = ["rate", "description", "is_active"]
        widgets = {
            "rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class HSNCodeForm(forms.ModelForm):
    class Meta:
        model = HSNCode
        fields = ["code", "description", "gst_rate", "is_active"]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "gst_rate": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class GSTSettingsForm(forms.ModelForm):
    class Meta:
        model = GSTSettings
        fields = ["business_name", "gstin", "state", "state_code",
                  "is_interstate", "financial_year_start"]
        widgets = {
            "business_name": forms.TextInput(attrs={"class": "form-control"}),
            "gstin": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "state_code": forms.TextInput(attrs={"class": "form-control"}),
            "is_interstate": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "financial_year_start": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
