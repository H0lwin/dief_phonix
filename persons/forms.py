from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Person, SalesInvoice, PurchaseInvoice
from datetime import date
from django.urls import reverse


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'phone_number_optional',
            'national_id',
            'address',
            'national_card_image',
            'description',
            'is_active',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('نام')
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('نام خانوادگی')
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('شماره تماس اولی'),
                'dir': 'ltr'
            }),
            'phone_number_optional': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('شماره تماس دوم'),
                'dir': 'ltr'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('کد ملی'),
                'dir': 'ltr'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('آدرس')
            }),
            'national_card_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('توضیحات')
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if national_id and len(national_id) != 10:
            raise forms.ValidationError(_('کد ملی باید 10 رقم باشد'))
        return national_id


class SalesInvoiceForm(forms.ModelForm):
    service_id = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control service-select',
            'id': 'id_service_id',
            'data-placeholder': _('ابتدا دسته‌بندی را انتخاب کنید'),
        }),
        label=_('خدمت'),
        choices=[]
    )
    
    class Meta:
        model = SalesInvoice
        fields = [
            'buyer',
            'invoice_date',
            'service_category',
            'service_id',
            'other_service_title',
            'sale_price',
            'settlement_type',
            'description',
            'is_active',
        ]
        widgets = {
            'buyer': forms.Select(attrs={
                'class': 'form-control',
            }),
            'invoice_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'service_category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_service_category',
            }),
            'other_service_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('عنوان خدمت دیگر'),
                'style': 'display: none;'
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('قیمت فروش'),
                'step': '0.01',
                'dir': 'ltr'
            }),
            'settlement_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('توضیحات')
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice_date'].initial = date.today()
        self.fields['service_id'].widget.choices = [('', '---------')]
        
        if self.instance.pk and self.instance.service_category and self.instance.service_id:
            self.populate_service_choices(self.instance.service_category)
            self.fields['service_id'].initial = str(self.instance.service_id)
    
    def populate_service_choices(self, service_type):
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
        
        model = model_map.get(service_type)
        if model:
            choices = [('', '---------')]
            if service_type == 'loan':
                for service in model.objects.filter(is_active=True).order_by('bank_name', 'plan_name'):
                    choices.append((str(service.id), str(service)))
            else:
                for service in model.objects.filter(is_active=True).order_by('name'):
                    choices.append((str(service.id), service.name))
            self.fields['service_id'].widget.choices = choices
    
    def clean(self):
        cleaned_data = super().clean()
        service_id = cleaned_data.get('service_id')
        if service_id and isinstance(service_id, str) and service_id.isdigit():
            cleaned_data['service_id'] = int(service_id)
        return cleaned_data


class PurchaseInvoiceForm(forms.ModelForm):
    service_id = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control service-select',
            'id': 'id_service_id',
            'data-placeholder': _('ابتدا دسته‌بندی را انتخاب کنید'),
        }),
        label=_('خدمت'),
        choices=[]
    )
    
    class Meta:
        model = PurchaseInvoice
        fields = [
            'vendor',
            'invoice_date',
            'service_category',
            'service_id',
            'other_service_title',
            'purchase_price',
            'settlement_type',
            'description',
            'is_active',
        ]
        widgets = {
            'vendor': forms.Select(attrs={
                'class': 'form-control',
            }),
            'invoice_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'service_category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_service_category',
            }),
            'other_service_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('عنوان خدمت دیگر'),
                'style': 'display: none;'
            }),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('قیمت خرید'),
                'step': '0.01',
                'dir': 'ltr'
            }),
            'settlement_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('توضیحات')
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice_date'].initial = date.today()
        self.fields['service_id'].widget.choices = [('', '---------')]
        
        if self.instance.pk and self.instance.service_category and self.instance.service_id:
            self.populate_service_choices(self.instance.service_category)
            self.fields['service_id'].initial = str(self.instance.service_id)
    
    def populate_service_choices(self, service_type):
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
        
        model = model_map.get(service_type)
        if model:
            choices = [('', '---------')]
            if service_type == 'loan':
                for service in model.objects.filter(is_active=True).order_by('bank_name', 'plan_name'):
                    choices.append((str(service.id), str(service)))
            else:
                for service in model.objects.filter(is_active=True).order_by('name'):
                    choices.append((str(service.id), service.name))
            self.fields['service_id'].widget.choices = choices
