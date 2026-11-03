from django import forms
from .models import Sale, SaleItem


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["sale_number", "sale_type", "customer", "sale_date", "location",
                  "billing_address", "shipping_address", "customer_gstin",
                  "discount_amount", "round_off", "notes", "status"]
        widgets = {
            "sale_number": forms.TextInput(attrs={"class": "form-control"}),
            "sale_type": forms.Select(attrs={"class": "form-select"}),
            "customer": forms.Select(attrs={"class": "form-select"}),
            "sale_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "location": forms.Select(attrs={"class": "form-select"}),
            "billing_address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "shipping_address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "customer_gstin": forms.TextInput(attrs={"class": "form-control"}),
            "discount_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "round_off": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


SaleItemFormSet = forms.inlineformset_factory(
    Sale, SaleItem, fields=["product", "quantity", "unit", "rate", "discount",
                            "gst_rate", "hsn_code"],
    widgets={
        "product": forms.Select(attrs={"class": "form-select"}),
        "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        "unit": forms.TextInput(attrs={"class": "form-control"}),
        "rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        "discount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        "gst_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        "hsn_code": forms.TextInput(attrs={"class": "form-control"}),
    },
    extra=3, can_delete=True,
)
