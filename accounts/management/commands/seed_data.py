from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import CustomUser
from persons.models import Person, SalesInvoice, PurchaseInvoice
from services.models import (
    LegalService,
    CommercialService,
    LeasingService,
    LoanService,
    RegistrationService,
)
from finance.models import ExpenseInvoice, IncomeInvoice, Salary
from factories import (
    CustomUserFactory,
    PersonFactory,
    SalesInvoiceFactory,
    PurchaseInvoiceFactory,
    LegalServiceFactory,
    CommercialServiceFactory,
    LeasingServiceFactory,
    LoanServiceFactory,
    RegistrationServiceFactory,
    ExpenseInvoiceFactory,
    IncomeInvoiceFactory,
    SalaryFactory,
)


class Command(BaseCommand):
    help = 'Seed database with realistic factory-generated data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--customers',
            type=int,
            default=200,
            help='Number of Person (customer) records to create'
        )
        parser.add_argument(
            '--services',
            type=int,
            default=50,
            help='Number of service records to create'
        )
        parser.add_argument(
            '--sales',
            type=int,
            default=300,
            help='Number of SalesInvoice records to create'
        )
        parser.add_argument(
            '--purchases',
            type=int,
            default=200,
            help='Number of PurchaseInvoice records to create'
        )
        parser.add_argument(
            '--employees',
            type=int,
            default=20,
            help='Number of Employee (CustomUser) records to create'
        )
        parser.add_argument(
            '--salaries',
            type=int,
            default=150,
            help='Number of Salary records to create'
        )
        parser.add_argument(
            '--expenses',
            type=int,
            default=100,
            help='Number of ExpenseInvoice records to create'
        )
        parser.add_argument(
            '--income',
            type=int,
            default=120,
            help='Number of IncomeInvoice records to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['clear']:
            self.clear_data()
            self.stdout.write(self.style.SUCCESS('[OK] Database cleared'))

        self.stdout.write(self.style.WARNING('\n[SEEDING] Starting database seeding...\n'))

        try:
            self.seed_employees(options['employees'])
            self.seed_services(options['services'])
            self.seed_customers(options['customers'])
            self.seed_sales_invoices(options['sales'])
            self.seed_purchase_invoices(options['purchases'])
            self.seed_salaries(options['salaries'])
            self.seed_expenses(options['expenses'])
            self.seed_income(options['income'])

            self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Database seeding completed successfully!\n'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n[ERROR] Error during seeding: {str(e)}\n'))
            raise

    def clear_data(self):
        """Clear existing data from database."""
        models = [
            SalesInvoice, PurchaseInvoice, Salary,
            ExpenseInvoice, IncomeInvoice,
            Person, CustomUser,
            LegalService, CommercialService,
            LeasingService, LoanService, RegistrationService,
        ]
        for model in models:
            model.objects.all().delete()

    def seed_employees(self, count):
        """Create employee records."""
        self.stdout.write(f'Creating {count} employees...')
        existing = CustomUser.objects.filter(role='admin').count()
        
        if existing >= count:
            self.stdout.write(self.style.WARNING(f'  Skipped (already {existing} employees)'))
            return
        
        to_create = count - existing
        CustomUserFactory.create_batch(to_create)
        self.stdout.write(self.style.SUCCESS(f'  [OK] Created {to_create} employees'))

    def seed_customers(self, count):
        """Create customer (Person) records."""
        self.stdout.write(f'Creating {count} customers...')
        existing = Person.objects.count()
        
        if existing >= count:
            self.stdout.write(self.style.WARNING(f'  Skipped (already {existing} customers)'))
            return
        
        to_create = count - existing
        PersonFactory.create_batch(to_create)
        self.stdout.write(self.style.SUCCESS(f'  [OK] Created {to_create} customers'))

    def seed_services(self, count):
        """Create service records."""
        self.stdout.write(f'Creating {count} services...')
        
        services_per_type = count // 5
        
        legal_count = LegalService.objects.count()
        if legal_count < services_per_type:
            LegalServiceFactory.create_batch(services_per_type - legal_count)
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created {services_per_type - legal_count} legal services'))
        
        commercial_count = CommercialService.objects.count()
        if commercial_count < services_per_type:
            CommercialServiceFactory.create_batch(services_per_type - commercial_count)
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created {services_per_type - commercial_count} commercial services'))
        
        registration_count = RegistrationService.objects.count()
        if registration_count < services_per_type:
            RegistrationServiceFactory.create_batch(services_per_type - registration_count)
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created {services_per_type - registration_count} registration services'))
        
        leasing_count = LeasingService.objects.count()
        if leasing_count < services_per_type:
            LeasingServiceFactory.create_batch(services_per_type - leasing_count)
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created {services_per_type - leasing_count} leasing services'))
        
        loan_count = LoanService.objects.count()
        if loan_count < services_per_type:
            LoanServiceFactory.create_batch(services_per_type - loan_count)
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created {services_per_type - loan_count} loan services'))

    def seed_sales_invoices(self, count):
        """Create sales invoice records."""
        self.stdout.write(f'Creating {count} sales invoices...')
        existing = SalesInvoice.objects.count()
        
        if existing >= count:
            self.stdout.write(self.style.WARNING(f'  Skipped (already {existing} invoices)'))
            return
        
        to_create = count - existing
        SalesInvoiceFactory.create_batch(to_create)
        self.stdout.write(self.style.SUCCESS(f'  [OK] Created {to_create} sales invoices'))

    def seed_purchase_invoices(self, count):
        """Create purchase invoice records."""
        self.stdout.write(f'Creating {count} purchase invoices...')
        existing = PurchaseInvoice.objects.count()
        
        if existing >= count:
            self.stdout.write(self.style.WARNING(f'  Skipped (already {existing} invoices)'))
            return
        
        to_create = count - existing
        PurchaseInvoiceFactory.create_batch(to_create)
        self.stdout.write(self.style.SUCCESS(f'  [OK] Created {to_create} purchase invoices'))

    def seed_salaries(self, count):
        """Create salary records."""
        self.stdout.write(f'Creating {count} salary records...')
        existing = Salary.objects.count()
        
        if existing >= count:
            self.stdout.write(self.style.WARNING(f'  Skipped (already {existing} salaries)'))
            return
        
        to_create = count - existing
        SalaryFactory.create_batch(to_create)
        self.stdout.write(self.style.SUCCESS(f'  [OK] Created {to_create} salary records'))

    def seed_expenses(self, count):
        """Create expense invoice records."""
        self.stdout.write(f'Creating {count} expense invoices...')
        existing = ExpenseInvoice.objects.count()
        
        if existing >= count:
            self.stdout.write(self.style.WARNING(f'  Skipped (already {existing} expenses)'))
            return
        
        to_create = count - existing
        ExpenseInvoiceFactory.create_batch(to_create)
        self.stdout.write(self.style.SUCCESS(f'  [OK] Created {to_create} expense invoices'))

    def seed_income(self, count):
        """Create income invoice records."""
        self.stdout.write(f'Creating {count} income invoices...')
        existing = IncomeInvoice.objects.count()
        
        if existing >= count:
            self.stdout.write(self.style.WARNING(f'  Skipped (already {existing} income)'))
            return
        
        to_create = count - existing
        IncomeInvoiceFactory.create_batch(to_create)
        self.stdout.write(self.style.SUCCESS(f'  [OK] Created {to_create} income invoices'))
