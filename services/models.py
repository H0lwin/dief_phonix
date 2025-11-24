from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractService(models.Model):
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('فعال')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاریخ ایجاد')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاریخ به‌روز‌رسانی')
    )
    
    class Meta:
        abstract = True


class LegalService(AbstractService):
    name = models.CharField(
        max_length=200,
        verbose_name=_('نام خدمت')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
    )
    
    class Meta:
        verbose_name = _('خدمت حقوقی')
        verbose_name_plural = _('خدمات حقوقی')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CommercialService(AbstractService):
    name = models.CharField(
        max_length=200,
        verbose_name=_('نام خدمت')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
    )
    
    class Meta:
        verbose_name = _('خدمت بازرگانی')
        verbose_name_plural = _('خدمات بازرگانی')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class LeasingService(AbstractService):
    name = models.CharField(
        max_length=200,
        verbose_name=_('نام خدمت')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
    )
    
    class Meta:
        verbose_name = _('خدمت لیزینگ')
        verbose_name_plural = _('خدمات لیزینگ')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class LoanService(AbstractService):
    bank_name = models.CharField(
        max_length=200,
        verbose_name=_('نام بانک عامل')
    )
    plan_name = models.CharField(
        max_length=200,
        verbose_name=_('نام طرح')
    )
    max_repayment_period = models.PositiveIntegerField(
        verbose_name=_('حداکثر مدت بازپرداخت (ماه)')
    )
    max_plan_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('حداکثر مبلغ طرح')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
    )
    
    class Meta:
        verbose_name = _('خدمت وام')
        verbose_name_plural = _('خدمات وام')
        ordering = ['bank_name', 'plan_name']
    
    def __str__(self):
        return f"{self.bank_name} - {self.plan_name}"


class RegistrationService(AbstractService):
    name = models.CharField(
        max_length=200,
        verbose_name=_('نام خدمت')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
    )
    
    class Meta:
        verbose_name = _('خدمت ثبت')
        verbose_name_plural = _('خدمات ثبت')
        ordering = ['name']
    
    def __str__(self):
        return self.name
