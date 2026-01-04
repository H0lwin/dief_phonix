from django.db import connection
import django
import os
import sys

# Add project root to path
sys.path.append('e:/phom/phonix_dashboard')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

with connection.cursor() as cursor:
    # finance_expenseinvoice
    try:
        cursor.execute('ALTER TABLE finance_expenseinvoice DROP FOREIGN KEY finance_expenseinvoi_created_by_id_4ed7d8f6_fk_accounts_')
        cursor.execute('ALTER TABLE finance_expenseinvoice DROP COLUMN created_by_id')
        print('Fixed finance_expenseinvoice')
    except Exception as e:
        print(f'Error fixing finance_expenseinvoice: {e}')
    
    # finance_incomeinvoice
    try:
        cursor.execute('ALTER TABLE finance_incomeinvoice DROP FOREIGN KEY finance_incomeinvoic_created_by_id_eb18029f_fk_accounts_')
        cursor.execute('ALTER TABLE finance_incomeinvoice DROP COLUMN created_by_id')
        print('Fixed finance_incomeinvoice')
    except Exception as e:
        print(f'Error fixing finance_incomeinvoice: {e}')
    
    # persons_person
    try:
        cursor.execute('ALTER TABLE persons_person DROP FOREIGN KEY persons_person_created_by_id_b461943e_fk_accounts_customuser_id')
        cursor.execute('ALTER TABLE persons_person DROP COLUMN created_by_id')
        print('Fixed persons_person')
    except Exception as e:
        print(f'Error fixing persons_person: {e}')
