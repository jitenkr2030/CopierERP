"""Seed a richer demo dataset: suppliers, customers, products, purchases, sales, calls."""
from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo transactions for a more populated dashboard."

    @transaction.atomic
    def handle(self, *args, **options):
        from companies.models import Company
        from products.models import Product, Category, Brand, Unit
        from purchases.models import Purchase, PurchaseItem
        from sales.models import Sale, SaleItem
        from crm.models import Call
        from requirements_app.models import Requirement, RequirementItem
        from inventory.models import StockLedger, Location
        from audit.utils import log_action
        from django.test import Client

        today = date.today()
        admin = User.objects.filter(is_superuser=True).first() or User.objects.first()

        # Make sure we have at least 5 companies
        companies_data = [
            ("COMP-101", "Acme Copiers Pvt Ltd", "customer", "Mumbai", "MH"),
            ("COMP-102", "BB INTERNATIONAL", "both", "Pune", "MH"),
            ("COMP-103", "SUN ENTERPRISES", "supplier", "Delhi", "DL"),
            ("COMP-104", "SS RAMJI ENTERPRISES", "supplier", "Bengaluru", "KA"),
            ("COMP-105", "D C COPIER SOLUTIONS PVT. LTD.", "customer", "Chennai", "TN"),
            ("COMP-106", "SharpTech Solutions", "customer", "Hyderabad", "TS"),
            ("COMP-107", "Konica Office Supplies", "supplier", "Kolkata", "WB"),
        ]
        for code, name, cat, city, state in companies_data:
            Company.objects.get_or_create(
                code=code,
                defaults={"name": name, "category": cat, "city": city,
                          "state": state, "country": "India",
                          "contact_person": name.split()[0],
                          "phone": "+91-9800000000",
                          "email": f"info@{name.split()[0].lower()}.com",
                          "gstin": f"27ABCDE{code[-3:]}1Z5"},
            )

        # Make sure products exist
        cat_toner = Category.objects.get_or_create(name="Toner")[0]
        cat_opc = Category.objects.get_or_create(name="OPC drum")[0]
        cat_drum = Category.objects.get_or_create(name="Drum")[0]
        cat_cartridge = Category.objects.get_or_create(name="Cartridge")[0]
        brand_canon = Brand.objects.get_or_create(name="Canon")[0]
        brand_hp = Brand.objects.get_or_create(name="HP")[0]
        brand_ricoh = Brand.objects.get_or_create(name="Ricoh")[0]
        unit_pcs = Unit.objects.get_or_create(name="Piece", defaults={"short": "Pcs"})[0]

        prods = [
            ("PRD-1001", "OPC Drum Canon IR2525", cat_opc, brand_canon, "OPC-CAN-2525-DM", 500, 750, 900, 10, 80),
            ("PRD-1002", "Toner Cartridge HP 12A (Demo)", cat_toner, brand_hp, "TON-HP-12A-DM", 800, 1250, 1500, 8, 50),
            ("PRD-1003", "Drum Unit Ricoh MP2014", cat_drum, brand_ricoh, "DRM-RIC-2014-DM", 1200, 1800, 2200, 5, 20),
            ("PRD-1004", "Canon IR2420 Cartridge", cat_cartridge, brand_canon, "CAR-CAN-2420-DM", 1500, 2200, 2600, 4, 12),
            ("PRD-1005", "HP 35A Toner", cat_toner, brand_hp, "TON-HP-35A-DM", 700, 1100, 1300, 6, 35),
        ]
        for code, name, cat, brand, sku, pr, sr, mrp, ms, cs in prods:
            p, created = Product.objects.get_or_create(
                code=code,
                defaults={"name": name, "category": cat, "brand": brand,
                          "sku": sku, "unit": unit_pcs,
                          "purchase_rate": pr, "sales_rate": sr, "mrp": mrp,
                          "minimum_stock": ms, "current_stock": cs,
                          "hsn_code": "84779000", "gst_rate": 18},
            )

        loc, _ = Location.objects.get_or_create(
            code="WH-MAIN", defaults={"name": "Main Warehouse"},
        )

        # Create 3 sample purchases (approved)
        sup1 = Company.objects.get(code="COMP-103")
        sup2 = Company.objects.get(code="COMP-104")
        sup3 = Company.objects.get(code="COMP-107")
        for i, (sup, prod_code, qty) in enumerate([
            (sup1, "PRD-1001", 20),
            (sup2, "PRD-1002", 30),
            (sup3, "PRD-1003", 15),
        ], start=1):
            pnum = f"PUR-DEMO-{i:03d}"
            if Purchase.objects.filter(purchase_number=pnum).exists():
                continue
            prod = Product.objects.get(code=prod_code)
            purchase = Purchase.objects.create(
                purchase_number=pnum, supplier=sup,
                supplier_invoice_no=f"SI-{i:03d}",
                purchase_date=today - timedelta(days=i),
                payment_method="credit", payment_status="unpaid",
                paid_amount=0, discount_amount=0,
                status="approved", created_by=admin, approved_by=admin,
                location=loc,
            )
            PurchaseItem.objects.create(
                purchase=purchase, product=prod, quantity=qty,
                unit="Piece", rate=prod.purchase_rate, discount=0,
                gst_rate=prod.gst_rate,
            )
            purchase.recalc()
            # Manually post stock
            StockLedger.append_entry(
                date=purchase.purchase_date, product=prod,
                transaction_type="purchase", transaction_id=pnum,
                transaction_model="Purchase", ref_pk=purchase.id,
                quantity_in=qty, company=sup, location=loc,
                rate=prod.purchase_rate, remarks=f"Purchase {pnum}", user=admin,
            )

        # Create 3 sample sales (confirmed)
        cust1 = Company.objects.get(code="COMP-101")
        cust2 = Company.objects.get(code="COMP-105")
        cust3 = Company.objects.get(code="COMP-106")
        for i, (cust, prod_code, qty) in enumerate([
            (cust1, "PRD-1002", 5),
            (cust2, "PRD-1005", 8),
            (cust3, "PRD-1001", 3),
        ], start=1):
            snum = f"SAL-DEMO-{i:03d}"
            if Sale.objects.filter(sale_number=snum).exists():
                continue
            prod = Product.objects.get(code=prod_code)
            sale = Sale.objects.create(
                sale_number=snum, sale_type="invoice", customer=cust,
                sale_date=today - timedelta(days=i),
                customer_gstin=cust.gstin, location=loc,
                discount_amount=0, round_off=0,
                status="confirmed", created_by=admin,
                billing_address=cust.address_line1 or f"{cust.city}, {cust.state}",
                shipping_address="",
            )
            SaleItem.objects.create(
                sale=sale, product=prod, quantity=qty, unit="Piece",
                rate=prod.sales_rate, discount=0, gst_rate=prod.gst_rate,
                hsn_code=prod.hsn_code,
            )
            sale.recalc()
            StockLedger.append_entry(
                date=sale.sale_date, product=prod,
                transaction_type="sales", transaction_id=snum,
                transaction_model="Sale", ref_pk=sale.id,
                quantity_out=qty, company=cust, location=loc,
                rate=prod.sales_rate, remarks=f"Sale {snum}", user=admin,
            )

        # Create sample calls
        for i, (cust, status) in enumerate([
            (cust1, "interested"),
            (cust2, "follow_up_pending"),
            (cust3, "completed"),
            (cust1, "requirement_received"),
            (cust2, "new"),
        ], start=1):
            cid = f"CALL-DEMO-{i:03d}"
            if Call.objects.filter(call_id=cid).exists():
                continue
            Call.objects.create(
                call_id=cid, company=cust, contact_person=cust.contact_person or "X",
                phone=cust.phone, call_date=today - timedelta(days=i),
                call_time="10:30", direction="outgoing", purpose="Enquiry",
                notes=f"Sample call {i}", next_follow_up=today + timedelta(days=2),
                status=status, assigned_to=admin, created_by=admin,
            )

        # Sample requirements
        for i, (cust, prod_code, qty) in enumerate([
            (cust1, "PRD-1001", 10),
            (cust2, "PRD-1003", 5),
        ], start=1):
            rnum = f"REQ-DEMO-{i:03d}"
            if Requirement.objects.filter(requirement_number=rnum).exists():
                continue
            r = Requirement.objects.create(
                requirement_number=rnum, company=cust,
                requirement_date=today - timedelta(days=i),
                priority="medium", expected_delivery_date=today + timedelta(days=7),
                assigned_to=admin, status="new", created_by=admin,
                remarks="Sample requirement",
            )
            RequirementItem.objects.create(
                requirement=r, product=Product.objects.get(code=prod_code),
                required_qty=qty, fulfilled_qty=0,
            )

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
