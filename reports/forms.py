from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import date
from persons.models import Person
from accounts.models import CustomUser
from .models import CustomerReport


class CustomerReportForm(forms.ModelForm):
    use_date_range = forms.BooleanField(
        required=False,
        initial=False,
        label=_('استفاده از بازه تاریخی'),
        help_text=_('اگر فعال کنید، بازه تاریخی استفاده می‌شود')
    )
    
    class Meta:
        model = CustomerReport
        fields = [
            'customer',
            'service_category',
            'service_id',
            'invoice_type',
            'settlement_type',
            'start_date',
            'end_date',
            'single_date',
            'filter_user',
        ]
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
            }),
            'service_category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_service_category_report',
            }),
            'service_id': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'service_id_display',
                'readonly': True,
                'placeholder': _('خدمت به صورت خودکار پر می‌شود'),
            }),
            'invoice_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'settlement_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_start_date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_end_date',
            }),
            'single_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'id_single_date',
                'style': 'display: none;',
            }),
            'filter_user': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'customer': _('مشتری'),
            'service_category': _('دسته‌بندی خدمت'),
            'service_id': _('خدمت'),
            'invoice_type': _('نوع فاکتور'),
            'settlement_type': _('نوع تسویه'),
            'start_date': _('تاریخ شروع'),
            'end_date': _('تاریخ پایان'),
            'single_date': _('تاریخ'),
            'filter_user': _('کاربر ثبت‌کننده'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make customer optional
        self.fields['customer'].required = False
        self.fields['customer'].empty_label = _('تمام مشتریان')
        
        # Filter active customers only
        self.fields['customer'].queryset = Person.objects.filter(is_active=True)
        
        # Filter active users only
        self.fields['filter_user'].required = False
        self.fields['filter_user'].empty_label = _('تمام کاربران')
        self.fields['filter_user'].queryset = CustomUser.objects.filter(is_active=True)
