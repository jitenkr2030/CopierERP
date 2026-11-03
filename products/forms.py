from django import forms
from .models import Product, Category, Brand, Unit


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name", "short", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "short": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["code", "name", "category", "brand", "model_no", "sku",
                  "barcode", "unit", "purchase_rate", "sales_rate", "mrp",
                  "minimum_stock", "current_stock", "reorder_qty",
                  "hsn_code", "gst_rate", "is_gst_applicable", "image",
                  "specifications", "is_active"]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "brand": forms.Select(attrs={"class": "form-select"}),
            "model_no": forms.TextInput(attrs={"class": "form-control"}),
            "sku": forms.TextInput(attrs={"class": "form-control"}),
            "barcode": forms.TextInput(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "purchase_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "sales_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "mrp": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "minimum_stock": forms.NumberInput(attrs={"class": "form-control"}),
            "current_stock": forms.NumberInput(attrs={"class": "form-control"}),
            "reorder_qty": forms.NumberInput(attrs={"class": "form-control"}),
            "hsn_code": forms.TextInput(attrs={"class": "form-control"}),
            "gst_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "is_gst_applicable": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "specifications": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
