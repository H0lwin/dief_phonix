from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
import os


class InvoiceNumberMixin:
    @staticmethod
    def generate_next_invoice_number(model_class):
        last_invoice = model_class.objects.order_by('-invoice_number').first()
        if last_invoice:
            return last_invoice.invoice_number + 1
        return 1000


class ExpenseInvoice(models.Model):
    invoice_number = models.PositiveIntegerField(
        unique=True,
        verbose_name=_('شماره فاکتور'),
        editable=False
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('مبلغ')
    )
    babet = models.CharField(
        max_length=255,
        verbose_name=_('بابت'),
        help_text=_('موضوع یا دلیل هزینه')
    )
    date = models.DateField(
        verbose_name=_('تاریخ')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
    )
    attachment = models.FileField(
        upload_to='finance/expense_invoices/',
        blank=True,
        null=True,
        verbose_name=_('فایل پیوست')
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
        verbose_name = _('فاکتور هزینه')
        verbose_name_plural = _('فاکتورهای هزینه')
        ordering = ['-date', '-invoice_number']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"فاکتور هزینه {self.invoice_number}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = InvoiceNumberMixin.generate_next_invoice_number(ExpenseInvoice)
        super().save(*args, **kwargs)


class IncomeInvoice(models.Model):
    invoice_number = models.PositiveIntegerField(
        unique=True,
        verbose_name=_('شماره فاکتور'),
        editable=False
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('مبلغ')
    )
    babet = models.CharField(
        max_length=255,
        verbose_name=_('بابت'),
        help_text=_('موضوع یا دلیل درآمد')
    )
    date = models.DateField(
        verbose_name=_('تاریخ')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
    )
    attachment = models.FileField(
        upload_to='finance/income_invoices/',
        blank=True,
        null=True,
        verbose_name=_('فایل پیوست')
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
        verbose_name = _('فاکتور درآمد')
        verbose_name_plural = _('فاکتورهای درآمد')
        ordering = ['-date', '-invoice_number']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"فاکتور درآمد {self.invoice_number}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = InvoiceNumberMixin.generate_next_invoice_number(IncomeInvoice)
        super().save(*args, **kwargs)


class Salary(models.Model):
    employee = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name=_('کارمند'),
        related_name='salaries'
    )
    date = models.DateField(
        verbose_name=_('تاریخ')
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_('مبلغ حقوق')
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name=_('پرداختی')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('توضیحات')
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
        verbose_name = _('حقوق')
        verbose_name_plural = _('حقوق‌ها')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['employee', 'date']),
            models.Index(fields=['is_paid']),
        ]
    
    def __str__(self):
        return f"حقوق {self.employee.get_display_name()} - {self.date}"
