from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def handle(self, *args, **options):
        username = 'H0lwin'
        email = 'Shayanqasmy88@gmail.com'
        password = 'Shayan.1400'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'سوپریوزر {username} قبلاً وجود دارد.')
            )
            return
        
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='شایان',
            last_name='قاسمی',
            role='admin'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'سوپریوزر {username} با موفقیت ایجاد شد.')
        )
        self.stdout.write(f'نام کاربری: {username}')
        self.stdout.write(f'ایمیل: {email}')
        self.stdout.write('رمز عبور: ******* (رمز ورودی شده)')
