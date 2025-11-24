from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.forms import ModelChoiceField
from .models import Person, SalesInvoice, PurchaseInvoice
from .forms import SalesInvoiceForm, PurchaseInvoiceForm
from accounts.admin import employee_admin_site
import json


class PersonAdmin(admin.ModelAdmin):
    list_display = [
        'get_full_name',
        'national_id',
        'phone_number',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'national_id',
        'phone_number',
    ]
    
    fieldsets = (
        (_('اطلاعات شخصی'), {
            'fields': (
                'first_name',
                'last_name',
                'national_id',
            )
        }),
        (_('اطلاعات تماس'), {
            'fields': (
                'phone_number',
                'phone_number_optional',
            )
        }),
        (_('آدرس و مستندات'), {
            'fields': (
                'address',
                'national_card_image',
            )
        }),
        (_('اطلاعات اضافی'), {
            'fields': (
                'description',
                'is_active',
            )
        }),
        (_('تاریخ‌های مهم'), {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    
    ordering = ['-created_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = _('نام کامل')


class SalesInvoiceAdmin(admin.ModelAdmin):
    form = SalesInvoiceForm
    
    list_display = [
        'invoice_number',
        'get_buyer_name',
        'invoice_date',
        'get_service_display',
        'sale_price',
        'settlement_type',
        'is_active',
    ]
    
    list_filter = [
        'invoice_date',
        'settlement_type',
        'service_category',
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'invoice_number',
        'buyer__first_name',
        'buyer__last_name',
        'buyer__national_id',
    ]
    
    fieldsets = (
        (_('اطلاعات فاکتور'), {
            'fields': (
                'invoice_number',
                'invoice_date',
                'buyer',
            )
        }),
        (_('خدمات'), {
            'fields': (
                'service_category',
                'service_id',
                'other_service_title',
            )
        }),
        (_('اطلاعات مالی'), {
            'fields': (
                'sale_price',
                'settlement_type',
            )
        }),
        (_('اطلاعات اضافی'), {
            'fields': (
                'description',
                'is_active',
            )
        }),
        (_('تاریخ‌های مهم'), {
            'fields': (
                'created_by',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'invoice_number',
        'created_at',
        'updated_at',
        'created_by',
    ]
    
    ordering = ['-invoice_date', '-invoice_number']
    
    class Media:
        css = {
            'all': ('css/service_modal.css',)
        }
        js = (
            'js/service_modal.js',
            'js/sales_invoice_admin.js',
        )
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'buyer':
            kwargs['queryset'] = Person.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_buyer_name(self, obj):
        return obj.buyer.get_full_name()
    get_buyer_name.short_description = _('خریدار')
    
    def get_service_display(self, obj):
        service = obj.get_service_object()
        if service:
            return service.name
        return obj.other_service_title or f'خدمت حذف شده ({obj.service_id})'
    get_service_display.short_description = _('خدمت')


class EmployeePersonAdmin(admin.ModelAdmin):
    list_display = [
        'get_full_name',
        'national_id',
        'phone_number',
        'is_active',
    ]
    
    list_filter = [
        'is_active',
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'national_id',
        'phone_number',
    ]
    
    fieldsets = (
        (_('اطلاعات شخصی'), {
            'fields': (
                'first_name',
                'last_name',
                'national_id',
            )
        }),
        (_('اطلاعات تماس'), {
            'fields': (
                'phone_number',
                'phone_number_optional',
            )
        }),
        (_('آدرس و مستندات'), {
            'fields': (
                'address',
                'national_card_image',
            )
        }),
        (_('اطلاعات اضافی'), {
            'fields': (
                'description',
                'is_active',
            )
        }),
    )
    
    readonly_fields = []
    
    ordering = ['-created_at']
    
    def has_module_permission(self, request):
        return True
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = _('نام کامل')


class EmployeeSalesInvoiceAdmin(admin.ModelAdmin):
    form = SalesInvoiceForm
    
    list_display = [
        'invoice_number',
        'get_buyer_name',
        'invoice_date',
        'get_service_display',
        'sale_price',
        'settlement_type',
    ]
    
    list_filter = [
        'invoice_date',
        'settlement_type',
        'service_category',
    ]
    
    search_fields = [
        'invoice_number',
        'buyer__first_name',
        'buyer__last_name',
        'buyer__national_id',
    ]
    
    fieldsets = (
        (_('اطلاعات فاکتور'), {
            'fields': (
                'invoice_number',
                'invoice_date',
                'buyer',
            )
        }),
        (_('خدمات'), {
            'fields': (
                'service_category',
                'service_id',
                'other_service_title',
            )
        }),
        (_('اطلاعات مالی'), {
            'fields': (
                'sale_price',
                'settlement_type',
            )
        }),
        (_('اطلاعات اضافی'), {
            'fields': (
                'description',
            )
        }),
    )
    
    readonly_fields = [
        'invoice_number',
    ]
    
    ordering = ['-invoice_date', '-invoice_number']
    
    class Media:
        css = {
            'all': ('css/service_modal.css',)
        }
        js = (
            'js/service_modal.js',
            'js/sales_invoice_admin.js',
        )
    
    def has_module_permission(self, request):
        return True
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_buyer_name(self, obj):
        return obj.buyer.get_full_name()
    get_buyer_name.short_description = _('خریدار')
    
    def get_service_display(self, obj):
        service = obj.get_service_object()
        if service:
            return service.name
        return obj.other_service_title or f'خدمت حذف شده ({obj.service_id})'
    get_service_display.short_description = _('خدمت')


class PurchaseInvoiceAdmin(admin.ModelAdmin):
    form = PurchaseInvoiceForm
    
    list_display = [
        'invoice_number',
        'get_vendor_name',
        'invoice_date',
        'get_service_display',
        'purchase_price',
        'settlement_type',
        'is_active',
    ]
    
    list_filter = [
        'invoice_date',
        'settlement_type',
        'service_category',
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'invoice_number',
        'vendor__first_name',
        'vendor__last_name',
        'vendor__national_id',
    ]
    
    fieldsets = (
        (_('اطلاعات فاکتور'), {
            'fields': (
                'invoice_number',
                'invoice_date',
                'vendor',
            )
        }),
        (_('خدمات'), {
            'fields': (
                'service_category',
                'service_id',
                'other_service_title',
            )
        }),
        (_('اطلاعات مالی'), {
            'fields': (
                'purchase_price',
                'settlement_type',
            )
        }),
        (_('اطلاعات اضافی'), {
            'fields': (
                'description',
                'is_active',
            )
        }),
        (_('تاریخ‌های مهم'), {
            'fields': (
                'created_by',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'invoice_number',
        'created_at',
        'updated_at',
        'created_by',
    ]
    
    ordering = ['-invoice_date', '-invoice_number']
    
    class Media:
        css = {
            'all': ('css/service_modal.css',)
        }
        js = (
            'js/service_modal.js',
            'js/purchase_invoice_admin.js',
        )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'vendor':
            kwargs['queryset'] = Person.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_vendor_name(self, obj):
        return obj.vendor.get_full_name()
    get_vendor_name.short_description = _('فروشنده')
    
    def get_service_display(self, obj):
        service = obj.get_service_object()
        if service:
            return service.name
        return obj.other_service_title or f'خدمت حذف شده ({obj.service_id})'
    get_service_display.short_description = _('خدمت')


class EmployeePurchaseInvoiceAdmin(admin.ModelAdmin):
    form = PurchaseInvoiceForm
    
    list_display = [
        'invoice_number',
        'get_vendor_name',
        'invoice_date',
        'get_service_display',
        'purchase_price',
        'settlement_type',
    ]
    
    list_filter = [
        'invoice_date',
        'settlement_type',
        'service_category',
    ]
    
    search_fields = [
        'invoice_number',
        'vendor__first_name',
        'vendor__last_name',
        'vendor__national_id',
    ]
    
    fieldsets = (
        (_('اطلاعات فاکتور'), {
            'fields': (
                'invoice_number',
                'invoice_date',
                'vendor',
            )
        }),
        (_('خدمات'), {
            'fields': (
                'service_category',
                'service_id',
                'other_service_title',
            )
        }),
        (_('اطلاعات مالی'), {
            'fields': (
                'purchase_price',
                'settlement_type',
            )
        }),
        (_('اطلاعات اضافی'), {
            'fields': (
                'description',
            )
        }),
    )
    
    readonly_fields = [
        'invoice_number',
    ]
    
    ordering = ['-invoice_date', '-invoice_number']
    
    class Media:
        css = {
            'all': ('css/service_modal.css',)
        }
        js = (
            'js/service_modal.js',
            'js/purchase_invoice_admin.js',
        )
    
    def has_module_permission(self, request):
        return True
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_vendor_name(self, obj):
        return obj.vendor.get_full_name()
    get_vendor_name.short_description = _('فروشنده')
    
    def get_service_display(self, obj):
        service = obj.get_service_object()
        if service:
            return service.name
        return obj.other_service_title or f'خدمت حذف شده ({obj.service_id})'
    get_service_display.short_description = _('خدمت')


admin.site.register(Person, PersonAdmin)
admin.site.register(SalesInvoice, SalesInvoiceAdmin)
admin.site.register(PurchaseInvoice, PurchaseInvoiceAdmin)

employee_admin_site.register(Person, EmployeePersonAdmin)
employee_admin_site.register(SalesInvoice, EmployeeSalesInvoiceAdmin)
employee_admin_site.register(PurchaseInvoice, EmployeePurchaseInvoiceAdmin)
