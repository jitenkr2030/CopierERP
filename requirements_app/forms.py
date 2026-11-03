from django import forms
from .models import Requirement, RequirementItem


class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ["requirement_number", "company", "requirement_date",
                  "priority", "expected_delivery_date", "assigned_to",
                  "status", "remarks"]
        widgets = {
            "requirement_number": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.Select(attrs={"class": "form-select"}),
            "requirement_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "expected_delivery_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "assigned_to": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


RequirementItemFormSet = forms.inlineformset_factory(
    Requirement, RequirementItem, fields=["product", "required_qty", "fulfilled_qty"],
    widgets={
        "product": forms.Select(attrs={"class": "form-select"}),
        "required_qty": forms.NumberInput(attrs={"class": "form-control"}),
        "fulfilled_qty": forms.NumberInput(attrs={"class": "form-control"}),
    },
    extra=3, can_delete=True,
)
