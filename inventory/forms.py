from django import forms
from .models import Location, StockAdjustment, StockTransfer


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["name", "code", "address", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class StockAdjustmentForm(forms.ModelForm):
    class Meta:
        model = StockAdjustment
        fields = ["date", "product", "location", "counted_qty", "reason", "remarks"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-select"}),
            "location": forms.Select(attrs={"class": "form-select"}),
            "counted_qty": forms.NumberInput(attrs={"class": "form-control"}),
            "reason": forms.Select(attrs={"class": "form-select"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class StockTransferForm(forms.ModelForm):
    class Meta:
        model = StockTransfer
        fields = ["date", "product", "from_location", "to_location", "quantity", "remarks"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "product": forms.Select(attrs={"class": "form-select"}),
            "from_location": forms.Select(attrs={"class": "form-select"}),
            "to_location": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
