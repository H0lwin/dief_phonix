import pytest
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

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


@pytest.mark.django_db
class TestCustomUserFactory:
    """Test CustomUser factory."""

    def test_create_user(self):
        """Test creating a single user."""
        user = CustomUserFactory()
        assert user.id is not None
        assert user.username.startswith('user_')
        assert user.first_name
        assert user.last_name
        assert user.email

    def test_create_user_with_phone(self):
        """Test user has valid phone number."""
        user = CustomUserFactory()
        assert user.phone_number is not None
        assert user.phone_number.startswith('09')

    def test_user_has_national_id(self):
        """Test user has unique national ID."""
        user1 = CustomUserFactory()
        user2 = CustomUserFactory()
        assert user1.national_id != user2.national_id

    def test_create_admin_user(self):
        """Test creating admin user with trait."""
        admin = CustomUserFactory(admin=True)
        assert admin.role == 'admin'
        assert admin.is_staff is True

    def test_create_superuser(self):
        """Test creating superuser."""
        superuser = CustomUserFactory(superuser=True)
        assert superuser.role == 'admin'
        assert superuser.is_staff is True
        assert superuser.is_superuser is True

    def test_user_password_set(self):
        """Test user password is properly set."""
        user = CustomUserFactory()
        assert user.has_usable_password()
        assert user.check_password('default_password_123')

    def test_create_batch_users(self):
        """Test creating multiple users."""
        users = CustomUserFactory.create_batch(10)
        assert len(users) == 10
        assert all(user.id for user in users)


@pytest.mark.django_db
class TestPersonFactory:
    """Test Person factory."""

    def test_create_person(self):
        """Test creating a single person."""
        person = PersonFactory()
        assert person.id is not None
        assert person.first_name
        assert person.last_name
        assert person.phone_number

    def test_person_national_id_unique(self):
        """Test person national IDs are unique."""
        person1 = PersonFactory()
        person2 = PersonFactory()
        assert person1.national_id != person2.national_id

    def test_person_phone_valid(self):
        """Test person phone numbers are valid Iranian numbers."""
        person = PersonFactory()
        assert person.phone_number.startswith('09')
        assert len(person.phone_number) == 11

    def test_person_has_address(self):
        """Test person has address."""
        person = PersonFactory()
        assert person.address is not None
        assert len(person.address) > 0

    def test_create_batch_persons(self):
        """Test creating multiple persons."""
        persons = PersonFactory.create_batch(50)
        assert len(persons) == 50
        assert all(p.id for p in persons)


@pytest.mark.django_db
class TestServiceFactories:
    """Test service factories."""

    def test_create_legal_service(self):
        """Test creating legal service."""
        service = LegalServiceFactory()
        assert service.id is not None
        assert service.name
        assert service.is_active is True

    def test_create_commercial_service(self):
        """Test creating commercial service."""
        service = CommercialServiceFactory()
        assert service.id is not None
        assert service.name
        assert service.is_active is True

    def test_create_registration_service(self):
        """Test creating registration service."""
        service = RegistrationServiceFactory()
        assert service.id is not None
        assert service.name
        assert service.is_active is True

    def test_create_leasing_service(self):
        """Test creating leasing service."""
        service = LeasingServiceFactory()
        assert service.id is not None
        assert service.name
        assert service.is_active is True

    def test_create_loan_service(self):
        """Test creating loan service."""
        service = LoanServiceFactory()
        assert service.id is not None
        assert service.bank_name
        assert service.plan_name
        assert service.max_repayment_period > 0
        assert service.max_plan_amount > 0


@pytest.mark.django_db
class TestInvoiceFactories:
    """Test invoice factories."""

    def test_create_sales_invoice(self):
        """Test creating sales invoice."""
        invoice = SalesInvoiceFactory()
        assert invoice.id is not None
        assert invoice.buyer is not None
        assert invoice.created_by is not None
        assert invoice.invoice_number > 0
        assert invoice.sale_price > 0

    def test_sales_invoice_number_unique(self):
        """Test sales invoice numbers are unique."""
        invoice1 = SalesInvoiceFactory()
        invoice2 = SalesInvoiceFactory()
        assert invoice1.invoice_number != invoice2.invoice_number

    def test_create_purchase_invoice(self):
        """Test creating purchase invoice."""
        invoice = PurchaseInvoiceFactory()
        assert invoice.id is not None
        assert invoice.vendor is not None
        assert invoice.created_by is not None
        assert invoice.invoice_number > 0
        assert invoice.purchase_price > 0

    def test_purchase_invoice_number_unique(self):
        """Test purchase invoice numbers are unique."""
        invoice1 = PurchaseInvoiceFactory()
        invoice2 = PurchaseInvoiceFactory()
        assert invoice1.invoice_number != invoice2.invoice_number

    def test_create_expense_invoice(self):
        """Test creating expense invoice."""
        invoice = ExpenseInvoiceFactory()
        assert invoice.id is not None
        assert invoice.invoice_number > 0
        assert invoice.amount > 0
        assert invoice.babet
        assert invoice.date

    def test_create_income_invoice(self):
        """Test creating income invoice."""
        invoice = IncomeInvoiceFactory()
        assert invoice.id is not None
        assert invoice.invoice_number > 0
        assert invoice.amount > 0
        assert invoice.babet
        assert invoice.date


@pytest.mark.django_db
class TestSalaryFactory:
    """Test Salary factory."""

    def test_create_salary(self):
        """Test creating salary record."""
        salary = SalaryFactory()
        assert salary.id is not None
        assert salary.employee is not None
        assert salary.amount > 0
        assert salary.date is not None

    def test_salary_employee_valid(self):
        """Test salary employee is valid CustomUser."""
        user = CustomUserFactory()
        salary = SalaryFactory(employee=user)
        assert salary.employee.id == user.id

    def test_create_batch_salaries(self):
        """Test creating multiple salary records."""
        salaries = SalaryFactory.create_batch(20)
        assert len(salaries) == 20
        assert all(s.id for s in salaries)


@pytest.mark.django_db
class TestFactoryRelationships:
    """Test factory relationships and foreign keys."""

    def test_sales_invoice_has_valid_buyer(self):
        """Test sales invoice buyer relationship."""
        invoice = SalesInvoiceFactory()
        assert isinstance(invoice.buyer, Person)
        assert invoice.buyer.id is not None

    def test_sales_invoice_has_valid_creator(self):
        """Test sales invoice creator relationship."""
        invoice = SalesInvoiceFactory()
        assert isinstance(invoice.created_by, CustomUser)
        assert invoice.created_by.id is not None

    def test_purchase_invoice_has_valid_vendor(self):
        """Test purchase invoice vendor relationship."""
        invoice = PurchaseInvoiceFactory()
        assert isinstance(invoice.vendor, Person)
        assert invoice.vendor.id is not None

    def test_salary_has_valid_employee(self):
        """Test salary employee relationship."""
        salary = SalaryFactory()
        assert isinstance(salary.employee, CustomUser)
        assert salary.employee.id is not None


@pytest.mark.django_db
class TestFactoryDataValidation:
    """Test factory-generated data validation."""

    def test_user_email_format(self):
        """Test generated email format is valid."""
        user = CustomUserFactory()
        assert '@' in user.email
        assert '.' in user.email.split('@')[1]

    def test_person_name_not_empty(self):
        """Test person names are not empty."""
        person = PersonFactory()
        assert len(person.first_name) > 0
        assert len(person.last_name) > 0

    def test_invoice_price_positive(self):
        """Test invoice prices are positive."""
        sales = SalesInvoiceFactory()
        purchase = PurchaseInvoiceFactory()
        assert sales.sale_price > 0
        assert purchase.purchase_price > 0

    def test_salary_amount_reasonable(self):
        """Test salary amounts are reasonable."""
        salary = SalaryFactory()
        assert salary.amount > 0
        assert salary.amount < Decimal('999999999999.99')

    def test_invoice_date_is_recent(self):
        """Test invoice dates are not far in future."""
        invoice = SalesInvoiceFactory()
        days_diff = (invoice.invoice_date - timezone.now().date()).days
        assert days_diff <= 1


@pytest.mark.django_db
class TestFactoryBatch:
    """Test batch factory creation."""

    def test_create_50_customers(self):
        """Test creating 50 customers."""
        customers = PersonFactory.create_batch(50)
        assert Person.objects.count() == 50
        assert len(customers) == 50

    def test_create_10_services_per_type(self):
        """Test creating multiple services."""
        legal = LegalServiceFactory.create_batch(10)
        commercial = CommercialServiceFactory.create_batch(10)
        assert len(legal) == 10
        assert len(commercial) == 10

    def test_create_complex_data_set(self):
        """Test creating complex interconnected data."""
        users = CustomUserFactory.create_batch(5)
        customers = PersonFactory.create_batch(20)
        services = {
            'legal': LegalServiceFactory.create_batch(5),
            'commercial': CommercialServiceFactory.create_batch(5),
        }
        invoices = SalesInvoiceFactory.create_batch(50)
        salaries = SalaryFactory.create_batch(30)

        assert CustomUser.objects.count() >= 5
        assert Person.objects.count() >= 20
        assert SalesInvoice.objects.count() >= 50
        assert Salary.objects.count() >= 30


@pytest.mark.django_db
class TestFactoryTraits:
    """Test factory trait usage."""

    def test_admin_trait_sets_correct_role(self):
        """Test admin trait sets admin role."""
        user = CustomUserFactory(admin=True)
        assert user.role == 'admin'
        assert user.is_staff is True

    def test_superuser_trait_sets_superuser(self):
        """Test superuser trait."""
        user = CustomUserFactory(superuser=True)
        assert user.is_superuser is True
        assert user.is_staff is True

    def test_person_with_optional_phone(self):
        """Test person factory with optional phone."""
        person = PersonFactory(with_optional_phone=True)
        assert person.phone_number_optional is not None


@pytest.mark.django_db
def test_complete_workflow():
    """Test a complete workflow using factories."""
    user = CustomUserFactory()
    customer = PersonFactory()
    service = CommercialServiceFactory()
    invoice = SalesInvoiceFactory(
        buyer=customer,
        created_by=user,
        service_id=service.id,
        service_category='commercial'
    )
    
    assert invoice.buyer.id == customer.id
    assert invoice.created_by.id == user.id
    assert invoice.service_id == service.id
    assert invoice.invoice_number > 1000


@pytest.mark.django_db
def test_fixture_usage(admin_user, customer_batch, all_services):
    """Test using pytest fixtures."""
    assert admin_user.is_superuser is False
    assert admin_user.role == 'admin'
    assert len(customer_batch) == 10
    assert 'legal' in all_services
    assert all_services['legal'].id is not None


@pytest.mark.django_db
def test_complete_dataset_fixture(complete_dataset):
    """Test complete dataset fixture."""
    assert len(complete_dataset['users']) >= 5
    assert len(complete_dataset['customers']) >= 10
    assert len(complete_dataset['sales_invoices']) >= 15
    assert len(complete_dataset['salaries']) >= 20
