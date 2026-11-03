"""Seed initial data: superuser + roles + sample catalog."""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = "Seed initial roles, superuser and demo catalog."

    @transaction.atomic
    def handle(self, *args, **options):
        # 1) Superuser
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin", email="admin@copier.erp",
                password="admin123", role="super_admin", employee_id="EMP-0001",
            )
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / admin123"))
        else:
            self.stdout.write("Superuser 'admin' already exists.")

        # 2) Sample users
        for uname, role in [("manager1", "manager"),
                             ("accountant1", "accountant"),
                             ("store1", "store_manager"),
                             ("emp1", "employee")]:
            if not User.objects.filter(username=uname).exists():
                User.objects.create_user(
                    username=uname, password="demo1234",
                    email=f"{uname}@copier.erp", role=role,
                )
                self.stdout.write(f"  created {uname} ({role}) demo1234")

        # 3) Categories
        from products.models import Category, Brand, Unit
        cats = ["Toner", "Drum", "OPC drum", "Cleaning blade", "Doctor blade",
                "Magnetic roller", "PCR", "Fuser assembly", "Pressure roller",
                "Developer", "Cartridge", "Copier spare parts", "Copier machines",
                "Other consumables"]
        for c in cats:
            Category.objects.get_or_create(name=c)

        for b in ["Canon", "HP", "Ricoh", "Konica Minolta", "Xerox",
                  "Sharp", "Kyocera", "Brother", "Samsung"]:
            Brand.objects.get_or_create(name=b)

        for name, short in [("Piece", "Pcs"), ("Box", "Box"),
                            ("Set", "Set"), ("Pack", "Pck")]:
            Unit.objects.get_or_create(name=name, defaults={"short": short})

        # 4) Sample companies (4 from the spec + extras)
        from companies.models import Company
        sample_companies = [
            ("D C COPIER SOLUTIONS PVT. LTD.", "COMP-006", "customer"),
            ("BB INTERNATIONAL", "COMP-005", "both"),
            ("SUN ENTERPRISES", "COMP-003", "supplier"),
            ("SS RAMJI ENTERPRISES", "COMP-002", "supplier"),
            ("Acme Copiers Pvt Ltd", "COMP-001", "customer"),
        ]
        for name, code, cat in sample_companies:
            Company.objects.get_or_create(
                code=code,
                defaults={"name": name, "category": cat, "city": "Mumbai",
                          "state": "MH", "country": "India"},
            )

        # 5) Sample products
        from products.models import Product
        cat_toner = Category.objects.get(name="Toner")
        cat_opc = Category.objects.get(name="OPC drum")
        cat_cartridge = Category.objects.get(name="Cartridge")
        brand_canon = Brand.objects.get(name="Canon")
        brand_hp = Brand.objects.get(name="HP")
        unit_pcs = Unit.objects.get(name="Piece")
        sample_products = [
            ("PRD-0001", "OPC Drum", cat_opc, brand_canon, "OPC-CAN-001", unit_pcs, 500, 750, 900, 10, 100),
            ("PRD-0002", "Toner Cartridge", cat_toner, brand_canon, "TON-CAN-001", unit_pcs, 1200, 1800, 2200, 5, 25),
            ("PRD-0003", "HP 12A Toner", cat_toner, brand_hp, "TON-HP-12A", unit_pcs, 800, 1250, 1500, 8, 50),
            ("PRD-0004", "Canon IR 2525 Drum", cat_cartridge, brand_canon, "DRM-CAN-2525", unit_pcs, 1500, 2200, 2600, 4, 12),
        ]
        for code, name, cat, brand, sku, unit, pr, sr, mrp, ms, cs in sample_products:
            Product.objects.get_or_create(
                code=code,
                defaults={"name": name, "category": cat, "brand": brand,
                          "sku": sku, "unit": unit, "purchase_rate": pr,
                          "sales_rate": sr, "mrp": mrp, "minimum_stock": ms,
                          "current_stock": cs, "hsn_code": "84779000",
                          "gst_rate": 18},
            )

        # 6) GST rates + HSN codes
        from gst.models import GSTRate, HSNCode
        for r in [0, 5, 12, 18, 28]:
            GSTRate.objects.get_or_create(rate=r)
        HSNCode.objects.get_or_create(
            code="84779000", defaults={"description": "Parts of machinery", "gst_rate_id": GSTRate.objects.get(rate=18).id},
        )

        # 7) Expense categories
        from expenses.models import ExpenseCategory
        for c in ["Office Expenses", "Salaries", "Rent", "Electricity",
                  "Telephone & Internet", "Travel", "Printing & Stationery",
                  "Bank Charges", "Miscellaneous"]:
            ExpenseCategory.objects.get_or_create(name=c)

        # 8) Inventory location
        from inventory.models import Location, StockLedger
        loc, _ = Location.objects.get_or_create(
            code="WH-MAIN", defaults={"name": "Main Warehouse"},
        )
        # Post opening stock for existing products
        from datetime import date
        today = date.today()
        for p in Product.objects.all():
            if not StockLedger.objects.filter(product=p, transaction_type="opening").exists() and p.current_stock:
                StockLedger.append_entry(
                    date=today, product=p, transaction_type="opening",
                    transaction_id=f"OPN-{p.code}", transaction_model="Manual",
                    quantity_in=p.current_stock, location=loc,
                    rate=p.purchase_rate, remarks="Opening stock",
                )

        self.stdout.write(self.style.SUCCESS("Seed complete."))
        self.stdout.write("Login: admin / admin123")
