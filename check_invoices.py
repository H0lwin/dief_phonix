#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from persons.models import SalesInvoice, PurchaseInvoice
from datetime import datetime

print("=" * 80)
print("SALES INVOICES (16-24 Nov 2025)")
print("=" * 80)
sales = SalesInvoice.objects.filter(
    invoice_date__gte='2025-11-16',
    invoice_date__lte='2025-11-24'
)
print(f"Total: {sales.count()}")
for inv in sales:
    print(f"ID: {inv.id}, Invoice: {inv.invoice_number}, Date: {inv.invoice_date}, Price: {inv.sale_price}, Created by: {inv.created_by_id}")

print("\n" + "=" * 80)
print("PURCHASE INVOICES (16-24 Nov 2025)")
print("=" * 80)
purchase = PurchaseInvoice.objects.filter(
    invoice_date__gte='2025-11-16',
    invoice_date__lte='2025-11-24'
)
print(f"Total: {purchase.count()}")
for inv in purchase:
    print(f"ID: {inv.id}, Invoice: {inv.invoice_number}, Date: {inv.invoice_date}, Price: {inv.purchase_price}, Created by: {inv.created_by_id}")

print("\n" + "=" * 80)
print("ALL SALES INVOICES (no filter)")
print("=" * 80)
all_sales = SalesInvoice.objects.all()
print(f"Total: {all_sales.count()}")
for inv in all_sales[:5]:
    print(f"ID: {inv.id}, Invoice: {inv.invoice_number}, Date: {inv.invoice_date}, Price: {inv.sale_price}, Created by: {inv.created_by_id}")

print("\n" + "=" * 80)
print("ALL PURCHASE INVOICES (no filter)")
print("=" * 80)
all_purchase = PurchaseInvoice.objects.all()
print(f"Total: {all_purchase.count()}")
for inv in all_purchase[:5]:
    print(f"ID: {inv.id}, Invoice: {inv.invoice_number}, Date: {inv.invoice_date}, Price: {inv.purchase_price}, Created by: {inv.created_by_id}")
