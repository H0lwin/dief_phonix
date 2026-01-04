from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from accounts.models import CustomUser, OwnedModel


ALLOWED_FILE_EXTENSIONS = [
    'zip', 'rar', 'pdf', 'xlsx', 'xls', 'doc', 'docx',
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp',
    'txt', 'csv', 'json'
]

ALLOWED_MIME_TYPES = [
    'application/zip',
    'application/x-rar-compressed',
    'application/x-7z-compressed',
    'application/x-tar',
    'application/gzip',
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/bmp',
    'image/webp',
    'text/plain',
    'text/csv',
    'application/json',
]


def validate_file_size_100mb(file):
    file_size = file.size
    limit_mb = 100
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(
            _('حجم فایل نمی‌تواند بیش‌تر از %(limit)s مگابایت باشد. حجم فایل شما: %(size).2f مگابایت') % {
                'limit': limit_mb,
                'size': file_size / (1024 * 1024),
            }
        )


def validate_file_type(file):
    import mimetypes
    
    file_name = file.name.lower()
    file_ext = file_name.split('.')[-1] if '.' in file_name else ''
    
    if file_ext not in ALLOWED_FILE_EXTENSIONS:
        extensions_list = ', '.join(ALLOWED_FILE_EXTENSIONS)
        raise ValidationError(
            _('نوع فایل "%(ext)s" مجاز نیست. فقط این نوع‌های فایل مجاز هستند: %(allowed)s') % {
                'ext': file_ext.upper(),
                'allowed': extensions_list,
            }
        )
    
    if hasattr(file, 'content_type'):
        mime_type = file.content_type
        if mime_type and mime_type not in ALLOWED_MIME_TYPES:
            raise ValidationError(
                _('نوع MIME فایل "%(mime)s" مجاز نیست.') % {
                    'mime': mime_type,
                }
            )


class Person(OwnedModel):
    first_name = models.CharField(
        max_length=200,
        verbose_name=_('نام')
    )
    last_name = models.CharField(
        max_length=200,
        verbose_name=_('نام خانوادگی')
    )
    phone_regex = RegexValidator(
        regex=r'^(\+98|0)?9\d{9}$',
        message=_('شماره تماس باید یک شماره موبایل معتبر ایرانی باشد')
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=12,
        verbose_name=_('شماره تماس اولی')
    )
    phone_number_optional = models.CharField(
        validators=[phone_regex],
        max_length=12,
        blank=True,
        null=True,
        verbose_name=_('شماره تماس دوم')
    )
    national_id = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_('کد ملی')
    )
    address = models.TextField(
        verbose_name=_('آدرس')
    )
    national_card_image = models.ImageField(
        upload_to='national_cards/',
        blank=True,
        null=True,
        verbose_name=_('تصویر کارت ملی')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
    )
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
        verbose_name = _('شخص')
        verbose_name_plural = _('اشخاص')
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['national_id']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['phone_number']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class SalesInvoice(OwnedModel):
    SERVICE_TYPE_CHOICES = [
        ('commercial', _('خدمات بازرگانی')),
        ('registration', _('خدمات ثبت')),
        ('legal', _('خدمات حقوقی')),
        ('leasing', _('خدمات لیزینگ')),
        ('loan', _('خدمات وام')),
    ]
    
    SETTLEMENT_CHOICES = [
        ('cash', _('نقدی')),
        ('conditional', _('شرایطی')),
    ]
    
    buyer = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name='invoices',
        verbose_name=_('خریدار')
    )
    invoice_number = models.PositiveIntegerField(
        unique=True,
        editable=False,
        verbose_name=_('شماره پرونده')
    )
    invoice_date = models.DateField(
        auto_now_add=False,
        verbose_name=_('تاریخ')
    )
    service_category = models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        verbose_name=_('دسته‌بندی خدمت')
    )
    service_id = models.PositiveIntegerField(
        verbose_name=_('خدمت'),
        null=True,
        blank=True
    )
    other_service_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('عنوان خدمت دیگر')
    )
    sale_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('قیمت فروش')
    )
    settlement_type = models.CharField(
        max_length=20,
        choices=SETTLEMENT_CHOICES,
        verbose_name=_('نوع تسویه')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
    )
    attachment = models.FileField(
        upload_to='sales_invoices/',
        blank=True,
        null=True,
        validators=[validate_file_size_100mb, validate_file_type],
        verbose_name=_('فایل پیوست'),
        help_text=_('حداکثر حجم: 100 مگابایت. فایل‌های مجاز: ZIP, RAR, PDF, Excel, Word, تصاویر و فایل‌های متنی')
    )
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
        verbose_name = _('فاکتور فروش')
        verbose_name_plural = _('فاکتورهای فروش')
        ordering = ['-invoice_date', '-invoice_number']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['invoice_date']),
            models.Index(fields=['buyer']),
        ]
    
    def __str__(self):
        return f"فاکتور {self.invoice_number} - {self.buyer.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_invoice = SalesInvoice.objects.order_by('-invoice_number').first()
            if last_invoice:
                self.invoice_number = last_invoice.invoice_number + 1
            else:
                self.invoice_number = 1000
        super().save(*args, **kwargs)
    
    def get_service_object(self):
        if not self.service_id or not self.service_category:
            return None
        
        from services.models import (
            CommercialService,
            RegistrationService,
            LegalService,
            LeasingService,
            LoanService
        )
        
        model_map = {
            'commercial': CommercialService,
            'registration': RegistrationService,
            'legal': LegalService,
            'leasing': LeasingService,
            'loan': LoanService,
        }
        
        model = model_map.get(self.service_category)
        if model:
            try:
                return model.objects.get(id=self.service_id)
            except model.DoesNotExist:
                return None
        return None


class PurchaseInvoice(OwnedModel):
    SERVICE_TYPE_CHOICES = [
        ('commercial', _('خدمات بازرگانی')),
        ('registration', _('خدمات ثبت')),
        ('legal', _('خدمات حقوقی')),
        ('leasing', _('خدمات لیزینگ')),
        ('loan', _('خدمات وام')),
    ]
    
    SETTLEMENT_CHOICES = [
        ('cash', _('نقدی')),
        ('conditional', _('شرایطی')),
    ]
    
    vendor = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name='purchase_invoices',
        verbose_name=_('فروشنده')
    )
    invoice_number = models.PositiveIntegerField(
        unique=True,
        editable=False,
        verbose_name=_('شماره پرونده')
    )
    invoice_date = models.DateField(
        auto_now_add=False,
        verbose_name=_('تاریخ')
    )
    service_category = models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        verbose_name=_('دسته‌بندی خدمت')
    )
    service_id = models.PositiveIntegerField(
        verbose_name=_('خدمت'),
        null=True,
        blank=True
    )
    other_service_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('عنوان خدمت دیگر')
    )
    purchase_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('قیمت خرید')
    )
    settlement_type = models.CharField(
        max_length=20,
        choices=SETTLEMENT_CHOICES,
        verbose_name=_('نوع تسویه')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
    )
    attachment = models.FileField(
        upload_to='purchase_invoices/',
        blank=True,
        null=True,
        validators=[validate_file_size_100mb, validate_file_type],
        verbose_name=_('فایل پیوست'),
        help_text=_('حداکثر حجم: 100 مگابایت. فایل‌های مجاز: ZIP, RAR, PDF, Excel, Word, تصاویر و فایل‌های متنی')
    )
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
        verbose_name = _('فاکتور خرید')
        verbose_name_plural = _('فاکتورهای خرید')
        ordering = ['-invoice_date', '-invoice_number']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['invoice_date']),
            models.Index(fields=['vendor']),
        ]
    
    def __str__(self):
        return f"فاکتور خرید {self.invoice_number} - {self.vendor.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_invoice = PurchaseInvoice.objects.order_by('-invoice_number').first()
            if last_invoice:
                self.invoice_number = last_invoice.invoice_number + 1
            else:
                self.invoice_number = 1000
        super().save(*args, **kwargs)
    
    def get_service_object(self):
        if not self.service_id or not self.service_category:
            return None
        
        from services.models import (
            CommercialService,
            RegistrationService,
            LegalService,
            LeasingService,
            LoanService
        )
        
        model_map = {
            'commercial': CommercialService,
            'registration': RegistrationService,
            'legal': LegalService,
            'leasing': LeasingService,
            'loan': LoanService,
        }
        
        model = model_map.get(self.service_category)
        if model:
            try:
                return model.objects.get(id=self.service_id)
            except model.DoesNotExist:
                return None
        return None
