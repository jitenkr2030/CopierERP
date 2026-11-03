from django import forms
from .models import Invoice


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["invoice_number", "invoice_type", "sale", "customer",
                  "invoice_date", "due_date", "total_amount", "paid_amount",
                  "is_paid", "notes"]
        widgets = {
            "invoice_number": forms.TextInput(attrs={"class": "form-control"}),
            "invoice_type": forms.Select(attrs={"class": "form-select"}),
            "sale": forms.Select(attrs={"class": "form-select"}),
            "customer": forms.Select(attrs={"class": "form-select"}),
            "invoice_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "total_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "paid_amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "is_paid": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
