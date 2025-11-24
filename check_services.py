#!/usr/bin/env python
import os
import django
import sys
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from services.models import CommercialService, RegistrationService, LegalService, LeasingService, LoanService

print("=" * 80)
print("COMMERCIAL SERVICES")
print("=" * 80)
services = CommercialService.objects.all()
print(f"Total: {services.count()}")
for service in services:
    print(f"ID: {service.id}, Name: {service.name}, Active: {service.is_active}")

print("\n" + "=" * 80)
print("REGISTRATION SERVICES")
print("=" * 80)
services = RegistrationService.objects.all()
print(f"Total: {services.count()}")
for service in services:
    print(f"ID: {service.id}, Name: {service.name}, Active: {service.is_active}")

print("\n" + "=" * 80)
print("LEGAL SERVICES")
print("=" * 80)
services = LegalService.objects.all()
print(f"Total: {services.count()}")
for service in services:
    print(f"ID: {service.id}, Name: {service.name}, Active: {service.is_active}")

print("\n" + "=" * 80)
print("LEASING SERVICES")
print("=" * 80)
services = LeasingService.objects.all()
print(f"Total: {services.count()}")
for service in services:
    print(f"ID: {service.id}, Name: {service.name}, Active: {service.is_active}")

print("\n" + "=" * 80)
print("LOAN SERVICES")
print("=" * 80)
services = LoanService.objects.all()
print(f"Total: {services.count()}")
for service in services:
    print(f"ID: {service.id}, Bank: {service.bank_name}, Plan: {service.plan_name}, Active: {service.is_active}")
