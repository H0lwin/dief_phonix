from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', _('ادمین')),
        ('user', _('کاربر')),
    ]
    
    STATUS_CHOICES = [
        ('active', _('فعال')),
        ('inactive', _('غیرفعال')),
        ('on_leave', _('مرخصی')),
        ('terminated', _('پایان‌یافته')),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_('شماره تلفن باید بین 9 تا 15 رقم باشد')
    )
    
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name=_('شماره تلفن')
    )
    
    national_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_('کد ملی')
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('ادرس محل سکونت')
    )
    
    position = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('سمت')
    )
    
    hire_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('تاریخ استخدام')
    )
    
    bank_account_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('شماره حساب بانکی')
    )
    
    document_file = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True,
        verbose_name=_('اپلود فایل')
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name=_('نقش')
    )
    
    current_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name=_('وضعیت فعلی')
    )
    
    is_active_status = models.BooleanField(
        default=True,
        verbose_name=_('وضعیت فعال')
    )
    
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('بیوگرافی')
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        verbose_name=_('تصویر پروفایل')
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
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['national_id']),
            models.Index(fields=['role']),
            models.Index(fields=['current_status']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name() or self.username}"
    
    def get_display_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username



