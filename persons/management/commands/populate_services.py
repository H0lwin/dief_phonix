from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from persons.models import ServiceCategory, Service


class Command(BaseCommand):
    help = 'Populate initial service categories and services'

    def handle(self, *args, **options):
        categories_data = [
            {
                'name': 'مشاوره',
                'description': 'خدمات مشاوره‌ای',
                'services': [
                    'مشاوره مالی',
                    'مشاوره حقوقی',
                    'مشاوره تکنیکی',
                ]
            },
            {
                'name': 'آموزش',
                'description': 'خدمات آموزشی',
                'services': [
                    'آموزش تخصصی',
                    'آموزش عمومی',
                    'آموزش آنلاین',
                ]
            },
            {
                'name': 'خدمات فنی',
                'description': 'خدمات تکنیکی و فنی',
                'services': [
                    'تعمیر و نگهداری',
                    'نصب و راه‌اندازی',
                    'پشتیبانی فنی',
                ]
            },
            {
                'name': 'خدمات طراحی',
                'description': 'خدمات طراحی و گرافیک',
                'services': [
                    'طراحی گرافیکی',
                    'طراحی صفحات وب',
                    'طراحی بسته‌بندی',
                ]
            },
        ]

        for category_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            
            if created:
                msg = 'Created category'
                self.stdout.write(self.style.SUCCESS(msg))
            
            for service_name in category_data['services']:
                service, service_created = Service.objects.get_or_create(
                    category=category,
                    name=service_name,
                )
                
                if service_created:
                    msg = 'Created service'
                    self.stdout.write(self.style.SUCCESS(msg))
        
        other_category, created = ServiceCategory.objects.get_or_create(
            name='سایر',
            defaults={'description': 'خدمات دیگر'}
        )
        
        if created:
            msg = 'Created category'
            self.stdout.write(self.style.SUCCESS(msg))
        
        other_service, service_created = Service.objects.get_or_create(
            category=other_category,
            name='سایر',
        )
        
        if service_created:
            msg = 'Created service'
            self.stdout.write(self.style.SUCCESS(msg))
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated services')
        )
