from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import LegalService, CommercialService, LeasingService, LoanService, RegistrationService


class LegalServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'name',
    ]
    
    fieldsets = (
        (_('اطلاعات خدمت'), {
            'fields': (
                'name',
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
    
    ordering = ['name']


class CommercialServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'name',
    ]
    
    fieldsets = (
        (_('اطلاعات خدمت'), {
            'fields': (
                'name',
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
    
    ordering = ['name']


class LeasingServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'name',
    ]
    
    fieldsets = (
        (_('اطلاعات خدمت'), {
            'fields': (
                'name',
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
    
    ordering = ['name']


class LoanServiceAdmin(admin.ModelAdmin):
    list_display = [
        'bank_name',
        'plan_name',
        'max_repayment_period',
        'max_plan_amount',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'bank_name',
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'bank_name',
        'plan_name',
    ]
    
    fieldsets = (
        (_('اطلاعات بانک و طرح'), {
            'fields': (
                'bank_name',
                'plan_name',
            )
        }),
        (_('شرایط طرح'), {
            'fields': (
                'max_repayment_period',
                'max_plan_amount',
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
    
    ordering = ['bank_name', 'plan_name']


class RegistrationServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'is_active',
        'created_at',
    ]
    
    list_filter = [
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'name',
    ]
    
    fieldsets = (
        (_('اطلاعات خدمت'), {
            'fields': (
                'name',
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
    
    ordering = ['name']


admin.site.register(LegalService, LegalServiceAdmin)
admin.site.register(CommercialService, CommercialServiceAdmin)
admin.site.register(LeasingService, LeasingServiceAdmin)
admin.site.register(LoanService, LoanServiceAdmin)
admin.site.register(RegistrationService, RegistrationServiceAdmin)
