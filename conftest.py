import os
import django
from django.conf import settings
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

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


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return CustomUserFactory(role='admin', is_staff=True, is_superuser=True)


@pytest.fixture
def regular_user(db):
    """Create a regular user."""
    return CustomUserFactory(role='user', is_staff=False)


@pytest.fixture
def user_batch(db):
    """Create a batch of users."""
    return CustomUserFactory.create_batch(5)


@pytest.fixture
def customer(db):
    """Create a customer (Person)."""
    return PersonFactory()


@pytest.fixture
def customer_batch(db):
    """Create a batch of customers."""
    return PersonFactory.create_batch(10)


@pytest.fixture
def legal_service(db):
    """Create a legal service."""
    return LegalServiceFactory()


@pytest.fixture
def commercial_service(db):
    """Create a commercial service."""
    return CommercialServiceFactory()


@pytest.fixture
def registration_service(db):
    """Create a registration service."""
    return RegistrationServiceFactory()


@pytest.fixture
def leasing_service(db):
    """Create a leasing service."""
    return LeasingServiceFactory()


@pytest.fixture
def loan_service(db):
    """Create a loan service."""
    return LoanServiceFactory()


@pytest.fixture
def all_services(
    db,
    legal_service,
    commercial_service,
    registration_service,
    leasing_service,
    loan_service
):
    """Create all types of services."""
    return {
        'legal': legal_service,
        'commercial': commercial_service,
        'registration': registration_service,
        'leasing': leasing_service,
        'loan': loan_service,
    }


@pytest.fixture
def sales_invoice(db, customer, regular_user):
    """Create a sales invoice."""
    return SalesInvoiceFactory(buyer=customer, created_by=regular_user)


@pytest.fixture
def sales_invoice_batch(db):
    """Create a batch of sales invoices."""
    return SalesInvoiceFactory.create_batch(5)


@pytest.fixture
def purchase_invoice(db, customer, regular_user):
    """Create a purchase invoice."""
    return PurchaseInvoiceFactory(vendor=customer, created_by=regular_user)


@pytest.fixture
def purchase_invoice_batch(db):
    """Create a batch of purchase invoices."""
    return PurchaseInvoiceFactory.create_batch(5)


@pytest.fixture
def expense_invoice(db):
    """Create an expense invoice."""
    return ExpenseInvoiceFactory()


@pytest.fixture
def expense_invoice_batch(db):
    """Create a batch of expense invoices."""
    return ExpenseInvoiceFactory.create_batch(5)


@pytest.fixture
def income_invoice(db):
    """Create an income invoice."""
    return IncomeInvoiceFactory()


@pytest.fixture
def income_invoice_batch(db):
    """Create a batch of income invoices."""
    return IncomeInvoiceFactory.create_batch(5)


@pytest.fixture
def salary(db, regular_user):
    """Create a salary record."""
    return SalaryFactory(employee=regular_user)


@pytest.fixture
def salary_batch(db):
    """Create a batch of salary records."""
    return SalaryFactory.create_batch(10)


@pytest.fixture
def complete_dataset(db):
    """Create a complete dataset for testing."""
    return {
        'users': CustomUserFactory.create_batch(5),
        'customers': PersonFactory.create_batch(10),
        'legal_services': LegalServiceFactory.create_batch(3),
        'commercial_services': CommercialServiceFactory.create_batch(3),
        'registration_services': RegistrationServiceFactory.create_batch(3),
        'leasing_services': LeasingServiceFactory.create_batch(3),
        'loan_services': LoanServiceFactory.create_batch(3),
        'sales_invoices': SalesInvoiceFactory.create_batch(15),
        'purchase_invoices': PurchaseInvoiceFactory.create_batch(10),
        'salaries': SalaryFactory.create_batch(20),
        'expenses': ExpenseInvoiceFactory.create_batch(10),
        'income': IncomeInvoiceFactory.create_batch(10),
    }


@pytest.mark.django_db
class TestFactoryGateway:
    """Base test class with factory access."""
    
    CustomUserFactory = CustomUserFactory
    PersonFactory = PersonFactory
    SalesInvoiceFactory = SalesInvoiceFactory
    PurchaseInvoiceFactory = PurchaseInvoiceFactory
    LegalServiceFactory = LegalServiceFactory
    CommercialServiceFactory = CommercialServiceFactory
    LeasingServiceFactory = LeasingServiceFactory
    LoanServiceFactory = LoanServiceFactory
    RegistrationServiceFactory = RegistrationServiceFactory
    ExpenseInvoiceFactory = ExpenseInvoiceFactory
    IncomeInvoiceFactory = IncomeInvoiceFactory
    SalaryFactory = SalaryFactory
