import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser
from django.utils.text import slugify

employees_data = [
    {
        'username': 'MOZHDE',
        'phone_number': '09336244434',
        'national_id': '2530149046',
        'position': 'کارشناس بازرگانی',
        'address': 'شیراز بلوار مدرس بلوار جانبازان',
        'hire_date': '2026-07-12',
        'bank_account_number': '8882',
    },
    {
        'username': 'Rasoul',
        'phone_number': '09178407177',
        'national_id': '2572170264',
        'position': 'کارمند',
        'address': 'بلوار نیستان انتهای کوچه 12 کوی مروارید غربی',
        'hire_date': '2026-07-09',
        'bank_account_number': '4540',
    },
    {
        'username': 'Reyhaneh',
        'phone_number': '09039273587',
        'national_id': '6700057027',
        'position': 'کارمند',
        'address': 'هفت تیر کوچه 6',
        'hire_date': None,
        'bank_account_number': '9199',
    },
    {
        'username': 'Nilofar',
        'phone_number': '09392974051',
        'national_id': '2283701139',
        'position': 'کارمند',
        'address': 'هفت تیر کوچه 6',
        'hire_date': None,
        'bank_account_number': '9173',
    },
    {
        'username': 'behnaz',
        'phone_number': '09371439632',
        'national_id': '5320105411',
        'position': 'کارمند',
        'address': None,
        'hire_date': '2025-10-29',
        'bank_account_number': '7273',
    },
]

def import_employees():
    created_count = 0
    skipped_count = 0
    
    for emp in employees_data:
        try:
            user, created = CustomUser.objects.get_or_create(
                username=emp['username'],
                defaults={
                    'email': f"{emp['username'].lower()}@dashboard.citysecret.ir",
                    'phone_number': emp['phone_number'],
                    'national_id': emp['national_id'],
                    'position': emp['position'],
                    'address': emp['address'],
                    'hire_date': emp['hire_date'],
                    'bank_account_number': emp['bank_account_number'],
                    'role': 'user',
                    'current_status': 'active',
                    'is_active': True,
                    'is_staff': False,
                    'is_superuser': False,
                }
            )
            
            if created:
                user.set_password(emp['username'])
                user.save()
                created_count += 1
                print(f"✓ ایجاد شد: {emp['username']} ({emp['position']})")
            else:
                skipped_count += 1
                print(f"⊘ موجود است: {emp['username']}")
                
        except Exception as e:
            print(f"✗ خطا برای {emp['username']}: {str(e)}")
    
    print(f"\n📊 نتایج:")
    print(f"   ✓ ایجاد شده: {created_count}")
    print(f"   ⊘ موجود: {skipped_count}")
    print(f"   📍 کل: {created_count + skipped_count}")

if __name__ == '__main__':
    import_employees()
