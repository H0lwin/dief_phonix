import factory
from factory import fuzzy
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random
from persons.models import Person, SalesInvoice, PurchaseInvoice
from accounts.models import CustomUser
from .base import get_iranian_faker
from .accounts import CustomUserFactory

fake = get_iranian_faker()

ServiceFactoryMap = {}


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    
    phone_number = factory.LazyFunction(lambda: fake.iranian_phone_number())
    phone_number_optional = factory.LazyFunction(
        lambda: fake.iranian_phone_number() if random.choice([True, False]) else None
    )
    
    national_id = factory.LazyFunction(lambda: fake.national_id())
    address = factory.LazyFunction(lambda: fake.address())
    
    description = factory.Faker('paragraph', nb_sentences=2)
    is_active = True
    
    created_at = factory.LazyFunction(
        lambda: timezone.now() - timedelta(days=random.randint(1, 365))
    )

    class Params:
        with_optional_phone = factory.Trait(
            phone_number_optional=factory.LazyFunction(lambda: fake.iranian_phone_number())
        )


class SalesInvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SalesInvoice

    buyer = factory.SubFactory(PersonFactory)
    created_by = factory.SubFactory(CustomUserFactory)
    
    invoice_date = factory.LazyFunction(
        lambda: (timezone.now() - timedelta(days=random.randint(1, 180))).date()
    )
    
    service_category = fuzzy.FuzzyChoice(
        ['commercial', 'registration', 'legal', 'leasing', 'loan']
    )
    
    service_id = factory.LazyAttribute(lambda o: None)
    other_service_title = factory.LazyFunction(
        lambda: fake.sentence() if random.choice([True, False]) else None
    )
    
    sale_price = factory.LazyFunction(
        lambda: Decimal(str(random.randint(1000000, 100000000)))
    )
    
    settlement_type = fuzzy.FuzzyChoice(['cash', 'conditional'])
    description = factory.Faker('paragraph', nb_sentences=2)
    is_active = True

    @factory.post_generation
    def set_service_id(obj, create, extracted, **kwargs):
        if not create or not obj.service_category:
            return
        
        from services.models import (
            CommercialService,
            RegistrationService,
            LegalService,
            LeasingService,
            LoanService
        )
        
        category_map = {
            'commercial': CommercialService,
            'registration': RegistrationService,
            'legal': LegalService,
            'leasing': LeasingService,
            'loan': LoanService,
        }
        
        service_model = category_map.get(obj.service_category)
        if service_model:
            service = service_model.objects.first()
            if not service:
                service = ServiceFactoryMap[obj.service_category].create()
            if service:
                obj.service_id = service.id
                obj.save()


class PurchaseInvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseInvoice

    vendor = factory.SubFactory(PersonFactory)
    created_by = factory.SubFactory(CustomUserFactory)
    
    invoice_date = factory.LazyFunction(
        lambda: (timezone.now() - timedelta(days=random.randint(1, 180))).date()
    )
    
    service_category = fuzzy.FuzzyChoice(
        ['commercial', 'registration', 'legal', 'leasing', 'loan']
    )
    
    service_id = factory.LazyAttribute(lambda o: None)
    other_service_title = factory.LazyFunction(
        lambda: fake.sentence() if random.choice([True, False]) else None
    )
    
    purchase_price = factory.LazyFunction(
        lambda: Decimal(str(random.randint(1000000, 100000000)))
    )
    
    settlement_type = fuzzy.FuzzyChoice(['cash', 'conditional'])
    description = factory.Faker('paragraph', nb_sentences=2)
    is_active = True

    @factory.post_generation
    def set_service_id(obj, create, extracted, **kwargs):
        if not create or not obj.service_category:
            return
        
        from services.models import (
            CommercialService,
            RegistrationService,
            LegalService,
            LeasingService,
            LoanService
        )
        
        category_map = {
            'commercial': CommercialService,
            'registration': RegistrationService,
            'legal': LegalService,
            'leasing': LeasingService,
            'loan': LoanService,
        }
        
        service_model = category_map.get(obj.service_category)
        if service_model:
            service = service_model.objects.first()
            if not service:
                service = ServiceFactoryMap[obj.service_category].create()
            if service:
                obj.service_id = service.id
                obj.save()
