# Copier Business ERP

A complete ERP for copier trading, distribution and consumables businesses — built with
**Python 3.12**, **Django 5.2** and **Django Ledger** as the double-entry accounting engine.

## Quick start

```bash
# 1) Create & activate virtualenv, then install deps
python -m venv .venv
source .venv/bin/activate         # Linux/Mac
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt

# 2) Copy .env.example to .env and edit DB credentials (defaults to SQLite)
cp .env.example .env

# 3) Run migrations & seed initial data
python manage.py migrate
python manage.py seed_data        # creates roles + superuser admin/admin123
python manage.py seed_demo        # optional: richer demo (companies, products, sales, calls)

# 4) Run dev server
python manage.py runserver
```

Open http://127.0.0.1:8000/ and log in as **admin / admin123**.

## Demo logins

| Username     | Role            | Password |
| ------------ | --------------- | -------- |
| admin        | Super Admin     | admin123 |
| manager1     | Manager         | demo1234 |
| accountant1  | Accountant      | demo1234 |
| store1       | Store Manager   | demo1234 |
| emp1         | Employee        | demo1234 |

## Accounting workflow (Django Ledger)

1. Log in as `admin` → visit **Accounting / Django Ledger** in the sidebar.
2. Click **Initialize Ledger** — creates a `django_ledger.EntityModel`,
   a chart of accounts (Cash, Bank, AR, Inventory, AP, GST Payable, Capital,
   Sales, COGS, Expenses) and a default General Ledger.
3. From now on every posted business transaction automatically creates a
   double-entry journal entry:
   - **Approved purchase** → Dr Inventory / Cr Accounts Payable
   - **Confirmed sale** → Dr Accounts Receivable / Cr Sales + Cr GST Payable
   - **Supplier payment** → Dr Accounts Payable / Cr Bank
   - **Customer receipt** → Dr Bank / Cr Accounts Receivable
   - **Expense booked** → Dr Expense / Cr Cash
4. Visit `/admin/django_ledger/` (or the native django_ledger views at `/ledger/`)
   to inspect the trial balance, P&L and balance sheet.

## Tech stack

| Layer            | Technology                |
| ---------------- | ------------------------- |
| Backend          | Python 3.12 + Django 5.2 |
| Accounting       | Django Ledger             |
| Frontend         | Django templates + Bootstrap 5 |
| Database         | SQLite (dev) / PostgreSQL (prod) |
| Excel            | openpyxl + pandas         |
| PDF              | ReportLab                 |
| Charts           | Chart.js via CDN          |
| API              | Django REST Framework     |

## Modules (21)

Dashboard, Users & Access, Companies, Customers, Suppliers, Products, Purchase,
Inventory, Stock Issue, Stock Returns, Sales, Invoicing, CRM (Calls),
Requirements, Payments, Accounting (Django Ledger), GST, Expenses, Reports,
Import/Export, Notifications, Audit Logs.

## Production checklist

- Set `DEBUG=False` and a strong `SECRET_KEY` in `.env`.
- Switch `DB_ENGINE` to `postgresql`.
- Run behind gunicorn + nginx.
- Configure Celery + Redis for async notifications if you enable background tasks.
