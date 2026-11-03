from django import forms
from .models import StockIssue, StockIssueItem


class StockIssueForm(forms.ModelForm):
    class Meta:
        model = StockIssue
        fields = ["issue_number", "company", "employee", "issue_date",
                  "location", "purpose", "reference_number", "remarks", "approval_status"]
        widgets = {
            "issue_number": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.Select(attrs={"class": "form-select"}),
            "employee": forms.Select(attrs={"class": "form-select"}),
            "issue_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "location": forms.Select(attrs={"class": "form-select"}),
            "purpose": forms.Select(attrs={"class": "form-select"}),
            "reference_number": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "approval_status": forms.Select(attrs={"class": "form-select"}),
        }


StockIssueItemFormSet = forms.inlineformset_factory(
    StockIssue, StockIssueItem, fields=["product", "quantity", "rate", "remarks"],
    widgets={
        "product": forms.Select(attrs={"class": "form-select"}),
        "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        "rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        "remarks": forms.TextInput(attrs={"class": "form-control"}),
    },
    extra=3, can_delete=True,
)
