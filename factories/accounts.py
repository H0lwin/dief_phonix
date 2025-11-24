import factory
from factory import fuzzy
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser
from .base import get_iranian_faker, POSITIONS

fake = get_iranian_faker()


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.Faker('email')
    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    
    phone_number = factory.LazyFunction(lambda: fake.iranian_phone_number())
    national_id = factory.LazyFunction(lambda: fake.national_id())
    
    address = factory.LazyFunction(lambda: fake.address())
    position = factory.LazyFunction(lambda: fake.random_element(POSITIONS))
    
    hire_date = factory.LazyFunction(
        lambda: (timezone.now() - timedelta(days=random_days())).date()
    )
    
    bank_account_number = factory.LazyFunction(lambda: fake.bank_account_number())
    
    role = fuzzy.FuzzyChoice(['admin', 'user'])
    current_status = fuzzy.FuzzyChoice(['active', 'inactive', 'on_leave', 'terminated'])
    is_active_status = True
    
    bio = factory.Faker('paragraph', nb_sentences=3)
    
    is_active = True
    is_staff = False
    is_superuser = False
    
    created_at = factory.LazyFunction(
        lambda: timezone.now() - timedelta(days=random_days(180))
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        obj.set_password('default_password_123')
        obj.save()
        return obj

    @factory.post_generation
    def groups(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                obj.groups.add(group)

    class Params:
        admin = factory.Trait(
            role='admin',
            is_staff=True,
            is_superuser=False,
        )
        
        superuser = factory.Trait(
            role='admin',
            is_staff=True,
            is_superuser=True,
        )


def random_days(max_days=365):
    """Generate random number of days."""
    import random
    return random.randint(1, max_days)
