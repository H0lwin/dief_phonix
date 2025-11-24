from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ExpenseInvoice, IncomeInvoice, Salary
from accounts.admin import employee_admin_site


class ExpenseInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number',
        'amount',
        'babet',
        'date',
        'created_at',
    ]
    
    list_filter = [
        'date',
        'created_at',
    ]
    
    search_fields = [
        'invoice_number',
        'babet',
        'description',
    ]
    
    fieldsets = (
        (_('اطلاعات فاکتور'), {
            'fields': (
                'invoice_number',
                'amount',
                'babet',
                'date',
            )
        }),
        (_('توضیحات و پیوست'), {
            'fields': (
                'description',
                'attachment',
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
        'invoice_number',
        'created_at',
        'updated_at',
    ]
    
    ordering = ['-date', '-invoice_number']


class IncomeInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number',
        'amount',
        'babet',
        'date',
        'created_at',
    ]
    
    list_filter = [
        'date',
        'created_at',
    ]
    
    search_fields = [
        'invoice_number',
        'babet',
        'description',
    ]
    
    fieldsets = (
        (_('اطلاعات فاکتور'), {
            'fields': (
                'invoice_number',
                'amount',
                'babet',
                'date',
            )
        }),
        (_('توضیحات و پیوست'), {
            'fields': (
                'description',
                'attachment',
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
        'invoice_number',
        'created_at',
        'updated_at',
    ]
    
    ordering = ['-date', '-invoice_number']


class EmployeeExpenseInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number',
        'amount',
        'babet',
        'date',
    ]
    
    list_filter = [
        'date',
    ]
    
    search_fields = [
        'invoice_number',
        'babet',
        'description',
    ]
    
    fieldsets = (
        (_('اطلاعات فاکتور'), {
            'fields': (
                'invoice_number',
                'amount',
                'babet',
                'date',
            )
        }),
        (_('توضیحات و پیوست'), {
            'fields': (
                'description',
                'attachment',
            )
        }),
    )
    
    readonly_fields = [
        'invoice_number',
    ]
    
    ordering = ['-date', '-invoice_number']
    
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


class EmployeeIncomeInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number',
        'amount',
        'babet',
        'date',
    ]
    
    list_filter = [
        'date',
    ]
    
    search_fields = [
        'invoice_number',
        'babet',
        'description',
    ]
    
    fieldsets = (
        (_('اطلاعات فاکتور'), {
            'fields': (
                'invoice_number',
                'amount',
                'babet',
                'date',
            )
        }),
        (_('توضیحات و پیوست'), {
            'fields': (
                'description',
                'attachment',
            )
        }),
    )
    
    readonly_fields = [
        'invoice_number',
    ]
    
    ordering = ['-date', '-invoice_number']
    
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


class SalaryAdmin(admin.ModelAdmin):
    list_display = [
        'get_employee_name',
        'date',
        'amount',
        'is_paid',
        'created_at',
    ]
    
    list_filter = [
        'date',
        'is_paid',
        'created_at',
    ]
    
    search_fields = [
        'employee__username',
        'employee__first_name',
        'employee__last_name',
        'description',
    ]
    
    fieldsets = (
        (_('اطلاعات کارمند'), {
            'fields': (
                'employee',
            )
        }),
        (_('اطلاعات حقوق'), {
            'fields': (
                'date',
                'amount',
                'is_paid',
            )
        }),
        (_('توضیحات'), {
            'fields': (
                'description',
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
    
    ordering = ['-date']
    
    def get_employee_name(self, obj):
        return obj.employee.get_display_name()
    get_employee_name.short_description = _('کارمند')


admin.site.register(ExpenseInvoice, ExpenseInvoiceAdmin)
admin.site.register(IncomeInvoice, IncomeInvoiceAdmin)
admin.site.register(Salary, SalaryAdmin)

employee_admin_site.register(ExpenseInvoice, EmployeeExpenseInvoiceAdmin)
employee_admin_site.register(IncomeInvoice, EmployeeIncomeInvoiceAdmin)
