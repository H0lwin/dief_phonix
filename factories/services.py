import factory
from decimal import Decimal
import random
from services.models import (
    LegalService,
    CommercialService,
    LeasingService,
    LoanService,
    RegistrationService,
)
from .base import get_iranian_faker, SERVICE_DESCRIPTIONS

fake = get_iranian_faker()


class LegalServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LegalService

    name = factory.LazyFunction(
        lambda: fake.random_element(SERVICE_DESCRIPTIONS['legal'])
    )
    description = factory.Faker('paragraph', nb_sentences=2)
    is_active = True


class CommercialServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommercialService

    name = factory.LazyFunction(
        lambda: fake.random_element(SERVICE_DESCRIPTIONS['commercial'])
    )
    description = factory.Faker('paragraph', nb_sentences=2)
    is_active = True


class RegistrationServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RegistrationService

    name = factory.LazyFunction(
        lambda: fake.random_element(SERVICE_DESCRIPTIONS['registration'])
    )
    description = factory.Faker('paragraph', nb_sentences=2)
    is_active = True


class LeasingServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LeasingService

    name = factory.LazyFunction(
        lambda: fake.random_element(SERVICE_DESCRIPTIONS['leasing'])
    )
    description = factory.Faker('paragraph', nb_sentences=2)
    is_active = True


class LoanServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LoanService

    bank_name = factory.LazyFunction(lambda: fake.bank_name())
    plan_name = factory.LazyFunction(
        lambda: fake.random_element([
            'طرح کارآفرین',
            'طرح توسعه‌ای',
            'طرح اقتصادی',
            'طرح سینا',
            'طرح کاسپین',
        ])
    )
    max_repayment_period = factory.LazyFunction(lambda: random.choice([12, 24, 36, 48, 60]))
    max_plan_amount = factory.LazyFunction(
        lambda: Decimal(str(random.randint(10000000, 500000000)))
    )
    description = factory.Faker('paragraph', nb_sentences=2)
    is_active = True


ServiceFactoryMap = {
    'legal': LegalServiceFactory,
    'commercial': CommercialServiceFactory,
    'registration': RegistrationServiceFactory,
    'leasing': LeasingServiceFactory,
    'loan': LoanServiceFactory,
}
