from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from persons.models import Person


class EmployeeReport(models.Model):
    employee = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='generated_reports',
        verbose_name=_('کارمند')
    )
    start_date = models.DateField(
        verbose_name=_('تاریخ شروع')
    )
    end_date = models.DateField(
        verbose_name=_('تاریخ پایان')
    )
    generated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reports_generated',
        verbose_name=_('تولید شده توسط')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاریخ ایجاد')
    )
    
    class Meta:
        verbose_name = _('گزارش کارمند')
        verbose_name_plural = _('گزارش‌های کارمند')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee', 'start_date', 'end_date']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"گزارش {self.employee.get_display_name()} ({self.start_date} تا {self.end_date})"


class FinancialReport(models.Model):
    start_date = models.DateField(
        verbose_name=_('تاریخ شروع')
    )
    end_date = models.DateField(
        verbose_name=_('تاریخ پایان')
    )
    generated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='financial_reports_generated',
        verbose_name=_('تولید شده توسط')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاریخ ایجاد')
    )
    
    class Meta:
        verbose_name = _('گزارش مالی')
        verbose_name_plural = _('گزارش‌های مالی')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"گزارش مالی ({self.start_date} تا {self.end_date})"


class CustomerReport(models.Model):
    INVOICE_TYPE_CHOICES = [
        ('all', _('هر دو')),
        ('sales', _('فقط فاکتور فروش')),
        ('purchase', _('فقط فاکتور خرید')),
    ]
    
    SETTLEMENT_TYPE_CHOICES = [
        ('all', _('هر دو')),
        ('cash', _('نقدی')),
        ('conditional', _('شرایطی')),
    ]
    
    SERVICE_CATEGORY_CHOICES = [
        ('', _('تمام دسته‌بندی‌ها')),
        ('commercial', _('خدمات بازرگانی')),
        ('registration', _('خدمات ثبت')),
        ('legal', _('خدمات حقوقی')),
        ('leasing', _('خدمات لیزینگ')),
        ('loan', _('خدمات وام')),
    ]
    
    customer = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='customer_reports',
        verbose_name=_('مشتری')
    )
    
    service_category = models.CharField(
        max_length=20,
        choices=SERVICE_CATEGORY_CHOICES,
        blank=True,
        default='',
        verbose_name=_('دسته‌بندی خدمت')
    )
    
    service_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('خدمت')
    )
    
    invoice_type = models.CharField(
        max_length=20,
        choices=INVOICE_TYPE_CHOICES,
        default='all',
        verbose_name=_('نوع فاکتور')
    )
    
    settlement_type = models.CharField(
        max_length=20,
        choices=SETTLEMENT_TYPE_CHOICES,
        default='all',
        verbose_name=_('نوع تسویه')
    )
    
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاریخ شروع')
    )
    
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاریخ پایان')
    )
    
    single_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاریخ واحد')
    )
    
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customer_reports_generated',
        verbose_name=_('کاربر ثبت‌کننده برای فیلتر')
    )
    
    generated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاریخ تولید گزارش')
    )
    
    generated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='generated_customer_reports',
        verbose_name=_('تولید شده توسط')
    )
    
    class Meta:
        verbose_name = _('گزارش مشتری')
        verbose_name_plural = _('گزارش‌های مشتری')
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['customer', 'generated_at']),
            models.Index(fields=['generated_at']),
        ]
    
    def __str__(self):
        customer_str = self.customer.get_full_name() if self.customer else 'همه مشتریان'
        return f"گزارش مشتری - {customer_str}"
