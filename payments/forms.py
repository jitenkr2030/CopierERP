from django import forms
from .models import Payment, Receipt, BankAccount


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["payment_number", "supplier", "purchase", "payment_date",
                  "amount", "method", "reference", "cheque_no", "cheque_date",
                  "bank", "notes"]
        widgets = {
            "payment_number": forms.TextInput(attrs={"class": "form-control"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "purchase": forms.Select(attrs={"class": "form-select"}),
            "payment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "method": forms.Select(attrs={"class": "form-select"}),
            "reference": forms.TextInput(attrs={"class": "form-control"}),
            "cheque_no": forms.TextInput(attrs={"class": "form-control"}),
            "cheque_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "bank": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ["receipt_number", "customer", "sale", "receipt_date",
                  "amount", "method", "reference", "cheque_no", "cheque_date",
                  "bank", "notes"]
        widgets = {
            "receipt_number": forms.TextInput(attrs={"class": "form-control"}),
            "customer": forms.Select(attrs={"class": "form-select"}),
            "sale": forms.Select(attrs={"class": "form-select"}),
            "receipt_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "method": forms.Select(attrs={"class": "form-select"}),
            "reference": forms.TextInput(attrs={"class": "form-control"}),
            "cheque_no": forms.TextInput(attrs={"class": "form-control"}),
            "cheque_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "bank": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["name", "bank_name", "account_number", "ifsc", "branch",
                  "opening_balance", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "bank_name": forms.TextInput(attrs={"class": "form-control"}),
            "account_number": forms.TextInput(attrs={"class": "form-control"}),
            "ifsc": forms.TextInput(attrs={"class": "form-control"}),
            "branch": forms.TextInput(attrs={"class": "form-control"}),
            "opening_balance": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
