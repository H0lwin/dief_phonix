import factory
from factory import fuzzy
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random
from finance.models import ExpenseInvoice, IncomeInvoice, Salary
from .base import get_iranian_faker, INVOICE_PURPOSES, SALARY_DESCRIPTIONS
from .accounts import CustomUserFactory

fake = get_iranian_faker()


class ExpenseInvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExpenseInvoice

    amount = factory.LazyFunction(
        lambda: Decimal(str(random.randint(100000, 50000000)))
    )
    babet = factory.LazyFunction(
        lambda: fake.random_element(INVOICE_PURPOSES)
    )
    date = factory.LazyFunction(
        lambda: (timezone.now() - timedelta(days=random.randint(1, 365))).date()
    )
    description = factory.Faker('paragraph', nb_sentences=2)


class IncomeInvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IncomeInvoice

    amount = factory.LazyFunction(
        lambda: Decimal(str(random.randint(100000, 50000000)))
    )
    babet = factory.LazyFunction(
        lambda: fake.random_element(INVOICE_PURPOSES[-6:])
    )
    date = factory.LazyFunction(
        lambda: (timezone.now() - timedelta(days=random.randint(1, 365))).date()
    )
    description = factory.Faker('paragraph', nb_sentences=2)


class SalaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Salary

    employee = factory.SubFactory(CustomUserFactory)
    
    date = factory.LazyFunction(
        lambda: (timezone.now() - timedelta(days=random.randint(1, 180))).date()
    )
    
    amount = factory.LazyFunction(
        lambda: Decimal(str(random.randint(5000000, 100000000)))
    )
    
    is_paid = factory.LazyFunction(lambda: random.choice([True] * 7 + [False] * 3))
    description = factory.LazyFunction(
        lambda: fake.random_element(SALARY_DESCRIPTIONS)
    )
