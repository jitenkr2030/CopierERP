from django import forms
from .models import StockReturn, StockReturnItem


class StockReturnForm(forms.ModelForm):
    class Meta:
        model = StockReturn
        fields = ["return_number", "issue", "company", "return_date",
                  "return_type", "remarks"]
        widgets = {
            "return_number": forms.TextInput(attrs={"class": "form-control"}),
            "issue": forms.Select(attrs={"class": "form-select"}),
            "company": forms.Select(attrs={"class": "form-select"}),
            "return_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "return_type": forms.Select(attrs={"class": "form-select"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


StockReturnItemFormSet = forms.inlineformset_factory(
    StockReturn, StockReturnItem, fields=["product", "quantity", "rate", "remarks"],
    widgets={
        "product": forms.Select(attrs={"class": "form-select"}),
        "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        "rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        "remarks": forms.TextInput(attrs={"class": "form-control"}),
    },
    extra=3, can_delete=True,
)
