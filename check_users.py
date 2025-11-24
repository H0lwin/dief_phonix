#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

print("=" * 80)
print("ALL USERS")
print("=" * 80)
users = CustomUser.objects.all()
print(f"Total: {users.count()}")
for user in users:
    print(f"ID: {user.id}, Username: {user.username}")
