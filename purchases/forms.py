from django import forms
from .models import Purchase, PurchaseItem


class PurchaseItemFormSetBase(forms.BaseInlineFormSet):
    pass


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["purchase_number", "supplier", "supplier_invoice_no",
                  "purchase_date", "location", "payment_method",
                  "payment_status", "paid_amount", "discount_amount",
                  "attachment", "notes", "status"]
        widgets = {
            "purchase_number": forms.TextInput(attrs={"class": "form-control"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "supplier_invoice_no": forms.TextInput(attrs={"class": "form-control"}),
            "purchase_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "location": forms.Select(attrs={"class": "form-select"}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
            "payment_status": forms.Select(attrs={"class": "form-select"}),
            "paid_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "discount_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "attachment": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


PurchaseItemFormSet = forms.inlineformset_factory(
    Purchase, PurchaseItem, fields=["product", "quantity", "unit", "rate",
                                     "discount", "gst_rate"],
    widgets={
        "product": forms.Select(attrs={"class": "form-select"}),
        "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        "unit": forms.TextInput(attrs={"class": "form-control"}),
        "rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        "discount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        "gst_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    },
    extra=3, can_delete=True,
)
