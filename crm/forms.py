from django import forms
from .models import Call, FollowUp


class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = ["call_id", "company", "contact_person", "phone",
                  "call_date", "call_time", "direction", "purpose",
                  "notes", "next_follow_up", "status", "assigned_to"]
        widgets = {
            "call_id": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.Select(attrs={"class": "form-select"}),
            "contact_person": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "call_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "call_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "direction": forms.Select(attrs={"class": "form-select"}),
            "purpose": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "next_follow_up": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "assigned_to": forms.Select(attrs={"class": "form-select"}),
        }


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ["date", "notes", "next_follow_up"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "next_follow_up": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
