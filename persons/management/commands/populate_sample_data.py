from django.core.management.base import BaseCommand
from django.utils import timezone
from persons.models import Person, SalesInvoice, ServiceCategory, Service
from datetime import date


class Command(BaseCommand):
    help = 'Populate sample persons and invoices for testing'

    def handle(self, *args, **options):
        sample_persons = [
            {
                'first_name': 'علی',
                'last_name': 'محمدی',
                'phone_number': '09121234567',
                'phone_number_optional': '09123456789',
                'national_id': '1234567890',
                'address': 'تهران، خیابان توحید، پلاک 42',
                'description': 'مشتری VIP'
            },
            {
                'first_name': 'فاطمه',
                'last_name': 'احمدی',
                'phone_number': '09131234567',
                'phone_number_optional': '',
                'national_id': '9876543210',
                'address': 'تهران، خیابان ولیعصر، پلاک 100',
                'description': 'مشتری نیمه‌فعال'
            },
        ]
        
        for person_data in sample_persons:
            person, created = Person.objects.get_or_create(
                national_id=person_data['national_id'],
                defaults={
                    'first_name': person_data['first_name'],
                    'last_name': person_data['last_name'],
                    'phone_number': person_data['phone_number'],
                    'phone_number_optional': person_data['phone_number_optional'],
                    'address': person_data['address'],
                    'description': person_data['description'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS('Created sample person'))
        
        persons = Person.objects.all()
        if persons.exists():
            person = persons.first()
            category = ServiceCategory.objects.first()
            service = Service.objects.first()
            
            if category and service:
                invoice, created = SalesInvoice.objects.get_or_create(
                    buyer=person,
                    invoice_date=date.today(),
                    defaults={
                        'service_category': category,
                        'service': service,
                        'sale_price': 500000,
                        'settlement_type': 'cash',
                        'description': 'فاکتور نمونه برای تست'
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS('Created sample invoice'))
        
        self.stdout.write(self.style.SUCCESS('Successfully populated sample data'))
