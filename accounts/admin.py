from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class EmployeeAdminSite(admin.AdminSite):
    site_header = _("پنل کارمندان")
    site_title = _("سیستم مدیریت کارمندان")
    index_title = _("خوش آمدید به پنل کارمندان")
    
    def has_permission(self, request):
        return request.user and request.user.is_active and not request.user.is_staff and not request.user.is_superuser
    
    def has_module_permission(self, request):
        return self.has_permission(request)


employee_admin_site = EmployeeAdminSite(name='employee-admin')


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    
    list_display = [
        'username',
        'email',
        'get_full_name_display',
        'position',
        'role',
        'current_status',
        'hire_date',
        'is_active',
    ]
    
    list_filter = [
        'position',
        'role',
        'current_status',
        'hire_date',
        'is_staff',
        'is_superuser',
        'is_active',
        'created_at',
    ]
    
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'national_id',
    ]
    
    fieldsets = (
        (_('اطلاعات شخصی'), {
            'fields': (
                'username',
                'password',
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'national_id',
                'bio',
                'profile_picture',
            )
        }),
        (_('اطلاعات محل کار'), {
            'fields': (
                'position',
                'hire_date',
                'address',
                'bank_account_number',
                'document_file',
            )
        }),
        (_('مجوزها'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
            'classes': ('collapse',)
        }),
        (_('اطلاعات نقش و وضعیت'), {
            'fields': (
                'role',
                'current_status',
                'is_active_status',
            )
        }),
        (_('تاریخ‌های مهم'), {
            'fields': (
                'last_login',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'email',
                'first_name',
                'last_name',
                'role',
            ),
        }),
    )
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'last_login',
    ]
    
    ordering = ['-created_at']
    
    def get_full_name_display(self, obj):
        return obj.get_display_name()
    get_full_name_display.short_description = _('نام کامل')
    
    def save_model(self, request, obj, form, change):
        if obj.role == 'admin':
            obj.is_staff = True
            obj.is_superuser = True
        super().save_model(request, obj, form, change)


class EmployeeCustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    
    list_display = [
        'username',
        'email',
        'get_full_name_display',
        'position',
        'phone_number',
        'is_active',
    ]
    
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'national_id',
    ]
    
    fieldsets = (
        (_('اطلاعات شخصی'), {
            'fields': (
                'username',
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'national_id',
                'bio',
                'profile_picture',
            )
        }),
        (_('اطلاعات محل کار'), {
            'fields': (
                'position',
                'hire_date',
                'address',
                'bank_account_number',
                'current_status',
            )
        }),
        (_('تاریخ‌های مهم'), {
            'fields': (
                'last_login',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'username',
        'created_at',
        'updated_at',
        'last_login',
        'position',
        'hire_date',
        'bank_account_number',
        'current_status',
    ]
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_full_name_display(self, obj):
        return obj.get_display_name()
    get_full_name_display.short_description = _('نام کامل')


admin.site.register(CustomUser, CustomUserAdmin)
