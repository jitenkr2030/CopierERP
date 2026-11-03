from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook


def _wb_response(wb, filename):
    from io import BytesIO
    out = BytesIO()
    wb.save(out)
    out.seek(0)
    resp = HttpResponse(out.getvalue(),
                        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp


class ImportExportIndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "imports_exports/index.html", {"segment": "import_export"})


def _export_companies():
    from companies.models import Company
    wb = Workbook(); ws = wb.active; ws.title = "Companies"
    ws.append(["Code", "Name", "Category", "Contact Person", "Phone", "Email",
               "City", "State", "GSTIN", "Credit Limit"])
    for c in Company.objects.all():
        ws.append([c.code, c.name, c.category, c.contact_person, c.phone, c.email,
                   c.city, c.state, c.gstin, float(c.credit_limit or 0)])
    return wb


def _export_products():
    from products.models import Product
    wb = Workbook(); ws = wb.active; ws.title = "Products"
    ws.append(["Code", "Name", "Category", "Brand", "SKU", "Unit",
               "Purchase Rate", "Sales Rate", "MRP", "Min Stock", "Current Stock",
               "HSN", "GST Rate"])
    for p in Product.objects.select_related("category", "brand", "unit"):
        ws.append([p.code, p.name, str(p.category), str(p.brand or ""),
                   p.sku, str(p.unit), float(p.purchase_rate), float(p.sales_rate),
                   float(p.mrp), p.minimum_stock, p.current_stock,
                   p.hsn_code, float(p.gst_rate)])
    return wb


def _export_purchases():
    from purchases.models import Purchase
    wb = Workbook(); ws = wb.active; ws.title = "Purchases"
    ws.append(["Number", "Supplier", "Date", "Subtotal", "GST", "Total", "Status"])
    for p in Purchase.objects.select_related("supplier"):
        ws.append([p.purchase_number, str(p.supplier), p.purchase_date.isoformat(),
                   float(p.subtotal or 0),
                   float((p.cgst_amount or 0)+(p.sgst_amount or 0)+(p.igst_amount or 0)),
                   float(p.total_amount or 0), p.status])
    return wb


def _export_sales():
    from sales.models import Sale
    wb = Workbook(); ws = wb.active; ws.title = "Sales"
    ws.append(["Number", "Customer", "Date", "Type", "Subtotal", "GST", "Total", "Status"])
    for s in Sale.objects.select_related("customer"):
        ws.append([s.sale_number, str(s.customer), s.sale_date.isoformat(), s.sale_type,
                   float(s.subtotal or 0),
                   float((s.cgst_amount or 0)+(s.sgst_amount or 0)+(s.igst_amount or 0)),
                   float(s.total_amount or 0), s.status])
    return wb


class ExportView(LoginRequiredMixin, View):
    def get(self, request, model):
        wb_map = {
            "companies": _export_companies,
            "products": _export_products,
            "purchases": _export_purchases,
            "sales": _export_sales,
        }
        fn = wb_map.get(model)
        if not fn:
            return HttpResponse("Unknown module", status=400)
        wb = fn()
        return _wb_response(wb, f"{model}.xlsx")


class ImportCompaniesView(LoginRequiredMixin, View):
    """Upload Excel for Companies; basic transactional insert."""
    template = "imports_exports/import_companies.html"

    def get(self, request):
        return render(request, self.template, {"segment": "import_export"})

    def post(self, request):
        f = request.FILES.get("file")
        if not f:
            return render(request, self.template,
                          {"segment": "import_export", "error": "No file uploaded"})
        wb = load_workbook(f, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(min_row=2, values_only=True))
        from companies.models import Company
        created, errors = 0, []
        for i, row in enumerate(rows, start=2):
            try:
                if not row or not row[0] or not row[1]:
                    continue
                Company.objects.update_or_create(
                    code=row[0],
                    defaults={
                        "name": row[1],
                        "category": row[2] or "other",
                        "contact_person": row[3] or "",
                        "phone": row[4] or "",
                        "email": row[5] or "",
                        "city": row[6] or "",
                        "state": row[7] or "",
                        "gstin": row[8] or "",
                        "credit_limit": row[9] or 0,
                    },
                )
                created += 1
            except Exception as exc:
                errors.append(f"Row {i}: {exc}")
        return render(request, self.template, {
            "segment": "import_export", "created": created, "errors": errors,
        })


class ImportProductsView(LoginRequiredMixin, View):
    template = "imports_exports/import_products.html"

    def get(self, request):
        return render(request, self.template, {"segment": "import_export"})

    def post(self, request):
        f = request.FILES.get("file")
        if not f:
            return render(request, self.template,
                          {"segment": "import_export", "error": "No file uploaded"})
        wb = load_workbook(f, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(min_row=2, values_only=True))
        from products.models import Product, Category, Brand, Unit
        created, errors = 0, []
        cat_other, _ = Category.objects.get_or_create(name="Imported")
        brand_other, _ = Brand.objects.get_or_create(name="Generic")
        unit_pcs, _ = Unit.objects.get_or_create(name="Piece", defaults={"short": "Pcs"})
        for i, row in enumerate(rows, start=2):
            try:
                if not row or not row[0] or not row[1]:
                    continue
                Product.objects.update_or_create(
                    code=row[0],
                    defaults={
                        "name": row[1],
                        "category": cat_other,
                        "brand": brand_other,
                        "sku": row[4] or row[0],
                        "unit": unit_pcs,
                        "purchase_rate": row[6] or 0,
                        "sales_rate": row[7] or 0,
                        "mrp": row[8] or 0,
                        "minimum_stock": row[9] or 0,
                        "current_stock": row[10] or 0,
                        "hsn_code": row[11] or "",
                        "gst_rate": row[12] or 18,
                    },
                )
                created += 1
            except Exception as exc:
                errors.append(f"Row {i}: {exc}")
        return render(request, self.template, {
            "segment": "import_export", "created": created, "errors": errors,
        })


class SampleTemplateView(LoginRequiredMixin, View):
    def get(self, request, model):
        wb = Workbook(); ws = wb.active
        if model == "companies":
            ws.append(["Code", "Name", "Category", "Contact Person", "Phone",
                       "Email", "City", "State", "GSTIN", "Credit Limit"])
            ws.append(["COMP-001", "Acme Copiers", "customer", "Ravi Kumar",
                       "+91-9876543210", "ravi@acme.com", "Mumbai", "MH",
                       "27ABCDE1234F1Z5", 100000])
        elif model == "products":
            ws.append(["Code", "Name", "Category", "Brand", "SKU", "Unit",
                       "Purchase Rate", "Sales Rate", "MRP", "Min Stock",
                       "Current Stock", "HSN", "GST Rate"])
            ws.append(["PRD-0001", "OPC Drum", "OPC drum", "Canon", "OPC-CAN-001",
                       "Piece", 500, 750, 900, 10, 100, "84779000", 18])
        else:
            return HttpResponse("Unknown template", status=400)
        return _wb_response(wb, f"template_{model}.xlsx")
