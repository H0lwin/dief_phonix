from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import models
from django.db.models import Q
from django.utils.html import format_html
from datetime import datetime, timedelta
import json
from .models import EmployeeReport, FinancialReport, CustomerReport
from persons.models import SalesInvoice, PurchaseInvoice
from finance.models import Salary
from accounts.models import CustomUser


class EmployeeReportAdmin(admin.ModelAdmin):
    list_display = [
        'get_employee_name',
        'start_date',
        'end_date',
        'get_total_activities',
        'created_at',
        'view_details_link',
    ]
    
    list_filter = [
        'employee',
        'created_at',
    ]
    
    search_fields = [
        'employee__username',
        'employee__first_name',
        'employee__last_name',
    ]
    
    fieldsets = (
        (_('انتخاب کارمند'), {
            'fields': (
                'employee',
            )
        }),
        (_('بازه تاریخی'), {
            'fields': (
                'start_date',
                'end_date',
            )
        }),
        (_('اطلاعات تولید'), {
            'fields': (
                'generated_by',
                'created_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'generated_by',
        'created_at',
    ]
    
    ordering = ['-created_at']
    
    def get_employee_name(self, obj):
        return obj.employee.get_display_name()
    get_employee_name.short_description = _('کارمند')
    
    def get_total_activities(self, obj):
        sales_count = SalesInvoice.objects.filter(
            created_by=obj.employee,
            invoice_date__gte=obj.start_date,
            invoice_date__lte=obj.end_date
        ).count()
        purchase_count = PurchaseInvoice.objects.filter(
            created_by=obj.employee,
            invoice_date__gte=obj.start_date,
            invoice_date__lte=obj.end_date
        ).count()
        return sales_count + purchase_count
    get_total_activities.short_description = _('تعداد فعالیت‌ها')
    
    def view_details_link(self, obj):
        url = reverse('admin:reports_employeereport_view_employee_report', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">{}</a>',
            url,
            _('مشاهده گزارش')
        )
    view_details_link.short_description = _('گزارش')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.generated_by = request.user
        super().save_model(request, obj, form, change)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_report_url'] = reverse('admin:reports_employeereport_generate_employee_report')
        extra_context['title'] = _('گزارش‌های کارمندان')
        return super().changelist_view(request, extra_context)
    
    change_list_template = 'admin/reports/employeereport_change_list.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:report_id>/report/',
                self.admin_site.admin_view(self.view_report),
                name='reports_employeereport_view_employee_report',
            ),
            path(
                'generate-report/',
                self.admin_site.admin_view(self.generate_report_form),
                name='reports_employeereport_generate_employee_report',
            ),
        ]
        return custom_urls + urls
    
    def view_report(self, request, report_id):
        report = get_object_or_404(EmployeeReport, pk=report_id)
        
        sales_invoices = SalesInvoice.objects.filter(
            created_by=report.employee,
            invoice_date__gte=report.start_date,
            invoice_date__lte=report.end_date
        ).select_related('buyer', 'created_by').order_by('-invoice_date')
        
        purchase_invoices = PurchaseInvoice.objects.filter(
            created_by=report.employee,
            invoice_date__gte=report.start_date,
            invoice_date__lte=report.end_date
        ).select_related('vendor', 'created_by').order_by('-invoice_date')
        
        salaries = Salary.objects.filter(
            employee=report.employee,
            date__gte=report.start_date,
            date__lte=report.end_date
        ).order_by('-date')
        
        paid_salaries = salaries.filter(is_paid=True)
        unpaid_salaries = salaries.filter(is_paid=False)
        total_salary_amount = sum(s.amount for s in salaries)
        paid_salary_amount = sum(s.amount for s in paid_salaries)
        unpaid_salary_amount = sum(s.amount for s in unpaid_salaries)
        
        context = {
            'report': report,
            'sales_invoices': sales_invoices,
            'purchase_invoices': purchase_invoices,
            'salaries': salaries,
            'paid_salaries_count': paid_salaries.count(),
            'unpaid_salaries_count': unpaid_salaries.count(),
            'total_salary_amount': total_salary_amount,
            'paid_salary_amount': paid_salary_amount,
            'unpaid_salary_amount': unpaid_salary_amount,
            'title': _('گزارش فعالیت‌های کارمند'),
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request),
        }
        
        response = TemplateResponse(
            request,
            'admin/reports/employee_report_detail.html',
            context,
        )
        response['Content-Type'] = 'text/html; charset=utf-8'
        return response
    
    def generate_report_form(self, request):
        if request.method == 'POST':
            employee_id = request.POST.get('employee')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            
            if employee_id and start_date and end_date:
                try:
                    employee = CustomUser.objects.get(pk=employee_id)
                    report = EmployeeReport.objects.create(
                        employee=employee,
                        start_date=start_date,
                        end_date=end_date,
                        generated_by=request.user
                    )
                    report_url = reverse('admin:reports_employeereport_view_employee_report', args=[report.id])
                    return redirect(report_url)
                except EmployeeReport.DoesNotExist:
                    pass
                except Exception as e:
                    pass
        
        employees = CustomUser.objects.filter(is_active=True).order_by('first_name', 'last_name')
        context = {
            'employees': employees,
            'title': _('تولید گزارش کارمند'),
            'opts': self.model._meta,
        }
        
        response = TemplateResponse(
            request,
            'admin/reports/generate_report_form.html',
            context,
        )
        response['Content-Type'] = 'text/html; charset=utf-8'
        return response


class FinancialReportAdmin(admin.ModelAdmin):
    list_display = [
        'date_range',
        'get_total_income',
        'get_total_expenses',
        'get_net_amount',
        'created_at',
        'view_details_link',
    ]
    
    list_filter = [
        'created_at',
    ]
    
    fieldsets = (
        (_('بازه تاریخی'), {
            'fields': (
                'start_date',
                'end_date',
            )
        }),
        (_('اطلاعات تولید'), {
            'fields': (
                'generated_by',
                'created_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'generated_by',
        'created_at',
    ]
    
    ordering = ['-created_at']
    
    change_list_template = 'admin/reports/financialreport_change_list.html'
    
    def date_range(self, obj):
        return f"{obj.start_date} تا {obj.end_date}"
    date_range.short_description = _('بازه تاریخی')
    
    def get_total_income(self, obj):
        total = SalesInvoice.objects.filter(
            invoice_date__gte=obj.start_date,
            invoice_date__lte=obj.end_date
        ).aggregate(total=models.Sum('sale_price'))['total'] or 0
        return f"{total:,.0f}"
    get_total_income.short_description = _('کل درامد')
    
    def get_total_expenses(self, obj):
        total = PurchaseInvoice.objects.filter(
            invoice_date__gte=obj.start_date,
            invoice_date__lte=obj.end_date
        ).aggregate(total=models.Sum('purchase_price'))['total'] or 0
        return f"{total:,.0f}"
    get_total_expenses.short_description = _('کل هزینه')
    
    def get_net_amount(self, obj):
        income = SalesInvoice.objects.filter(
            invoice_date__gte=obj.start_date,
            invoice_date__lte=obj.end_date
        ).aggregate(total=models.Sum('sale_price'))['total'] or 0
        expenses = PurchaseInvoice.objects.filter(
            invoice_date__gte=obj.start_date,
            invoice_date__lte=obj.end_date
        ).aggregate(total=models.Sum('purchase_price'))['total'] or 0
        net = income - expenses
        return f"{net:,.0f}"
    get_net_amount.short_description = _('خالص')
    
    def view_details_link(self, obj):
        url = reverse('admin:reports_financialreport_view_financial_report', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">{}</a>',
            url,
            _('مشاهده گزارش')
        )
    view_details_link.short_description = _('گزارش')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.generated_by = request.user
        super().save_model(request, obj, form, change)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_report_url'] = reverse('admin:reports_financialreport_generate_financial_report')
        extra_context['title'] = _('گزارش‌های مالی')
        return super().changelist_view(request, extra_context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:report_id>/report/',
                self.admin_site.admin_view(self.view_report),
                name='reports_financialreport_view_financial_report',
            ),
            path(
                'generate-report/',
                self.admin_site.admin_view(self.generate_report_form),
                name='reports_financialreport_generate_financial_report',
            ),
        ]
        return custom_urls + urls
    
    def view_report(self, request, report_id):
        report = get_object_or_404(FinancialReport, pk=report_id)
        
        sales_invoices = SalesInvoice.objects.filter(
            invoice_date__gte=report.start_date,
            invoice_date__lte=report.end_date
        ).select_related('created_by', 'buyer').order_by('-invoice_date')
        
        purchase_invoices = PurchaseInvoice.objects.filter(
            invoice_date__gte=report.start_date,
            invoice_date__lte=report.end_date
        ).select_related('created_by', 'vendor').order_by('-invoice_date')
        
        total_income = sum(inv.sale_price for inv in sales_invoices)
        total_expenses = sum(inv.purchase_price for inv in purchase_invoices)
        net_amount = total_income - total_expenses
        
        sales_count = sales_invoices.count()
        purchase_count = purchase_invoices.count()
        total_invoices = sales_count + purchase_count
        
        context = {
            'report': report,
            'sales_invoices': sales_invoices,
            'purchase_invoices': purchase_invoices,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_amount': net_amount,
            'sales_count': sales_count,
            'purchase_count': purchase_count,
            'total_invoices': total_invoices,
            'title': _('گزارش مالی'),
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request),
        }
        
        response = TemplateResponse(
            request,
            'admin/reports/financial_report_detail.html',
            context,
        )
        response['Content-Type'] = 'text/html; charset=utf-8'
        return response
    
    def generate_report_form(self, request):
        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            
            if start_date and end_date:
                try:
                    report = FinancialReport.objects.create(
                        start_date=start_date,
                        end_date=end_date,
                        generated_by=request.user
                    )
                    report_url = reverse('admin:reports_financialreport_view_financial_report', args=[report.id])
                    return redirect(report_url)
                except Exception as e:
                    pass
        
        context = {
            'title': _('تولید گزارش مالی'),
            'opts': self.model._meta,
        }
        
        response = TemplateResponse(
            request,
            'admin/reports/generate_financial_report_form.html',
            context,
        )
        response['Content-Type'] = 'text/html; charset=utf-8'
        return response


class CustomerReportAdmin(admin.ModelAdmin):
    list_display = [
        'get_customer_name',
        'service_category',
        'invoice_type',
        'settlement_type',
        'generated_at',
        'view_details_link',
    ]
    
    list_filter = [
        'customer',
        'service_category',
        'invoice_type',
        'settlement_type',
        'generated_at',
    ]
    
    search_fields = [
        'customer__first_name',
        'customer__last_name',
        'customer__national_id',
    ]
    
    fieldsets = (
        (_('فیلتر مشتری'), {
            'fields': (
                'customer',
            )
        }),
        (_('فیلتر خدمات'), {
            'fields': (
                'service_category',
                'service_id',
            )
        }),
        (_('فیلتر نوع فاکتور و تسویه'), {
            'fields': (
                'invoice_type',
                'settlement_type',
            )
        }),
        (_('فیلتر تاریخ'), {
            'fields': (
                'single_date',
                'start_date',
                'end_date',
            )
        }),
        (_('فیلتر کاربر'), {
            'fields': (
                'created_by',
            )
        }),
        (_('اطلاعات تولید'), {
            'fields': (
                'generated_by',
                'generated_at',
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'generated_by',
        'generated_at',
    ]
    
    ordering = ['-generated_at']
    
    change_list_template = 'admin/reports/customerreport_change_list.html'
    
    def get_customer_name(self, obj):
        if obj.customer:
            return obj.customer.get_full_name()
        return _('همه مشتریان')
    get_customer_name.short_description = _('مشتری')
    
    def view_details_link(self, obj):
        url = reverse('admin:reports_customerreport_view_customer_report', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">{}</a>',
            url,
            _('مشاهده گزارش')
        )
    view_details_link.short_description = _('نمایش')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.generated_by = request.user
        super().save_model(request, obj, form, change)
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_report_url'] = reverse('admin:reports_customerreport_generate_customer_report')
        extra_context['title'] = _('گزارش‌های مشتری')
        return super().changelist_view(request, extra_context)
    
    def get_urls(self):
        from services.models import (
            CommercialService, RegistrationService, LegalService,
            LeasingService, LoanService
        )
        
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:report_id>/report/',
                self.admin_site.admin_view(self.view_report),
                name='reports_customerreport_view_customer_report',
            ),
            path(
                'generate-report/',
                self.admin_site.admin_view(self.generate_report_form),
                name='reports_customerreport_generate_customer_report',
            ),
            path(
                'api/services-by-category/',
                self.admin_site.admin_view(self.api_services_by_category),
                name='reports_customerreport_api_services',
            ),
        ]
        return custom_urls + urls
    
    def view_report(self, request, report_id):
        from services.models import (
            CommercialService, RegistrationService, LegalService,
            LeasingService, LoanService
        )
        
        report = get_object_or_404(CustomerReport, pk=report_id)
        
        sales_query = SalesInvoice.objects.all()
        purchase_query = PurchaseInvoice.objects.all()
        
        if report.customer:
            sales_query = sales_query.filter(buyer=report.customer)
            purchase_query = purchase_query.filter(vendor=report.customer)
        
        if report.service_category:
            sales_query = sales_query.filter(service_category=report.service_category)
            purchase_query = purchase_query.filter(service_category=report.service_category)
        
        if report.service_id:
            sales_query = sales_query.filter(service_id=report.service_id)
            purchase_query = purchase_query.filter(service_id=report.service_id)
        
        if report.settlement_type != 'all':
            sales_query = sales_query.filter(settlement_type=report.settlement_type)
            purchase_query = purchase_query.filter(settlement_type=report.settlement_type)
        
        if report.single_date:
            sales_query = sales_query.filter(invoice_date=report.single_date)
            purchase_query = purchase_query.filter(invoice_date=report.single_date)
        elif report.start_date and report.end_date:
            sales_query = sales_query.filter(
                invoice_date__gte=report.start_date,
                invoice_date__lte=report.end_date
            )
            purchase_query = purchase_query.filter(
                invoice_date__gte=report.start_date,
                invoice_date__lte=report.end_date
            )
        
        if report.created_by:
            sales_query = sales_query.filter(created_by=report.created_by)
            purchase_query = purchase_query.filter(created_by=report.created_by)
        
        invoices = []
        
        if report.invoice_type in ['sales', 'all']:
            for invoice in sales_query.select_related('buyer', 'created_by'):
                service_obj = self.get_service_object(invoice.service_id, invoice.service_category)
                invoices.append({
                    'type': _('فروش'),
                    'invoice_number': invoice.invoice_number,
                    'invoice_date': invoice.invoice_date,
                    'customer_first_name': invoice.buyer.first_name,
                    'customer_last_name': invoice.buyer.last_name,
                    'service_category': invoice.get_service_category_display(),
                    'service_name': service_obj.name if service_obj else (invoice.other_service_title or _('نامشخص')),
                    'settlement_type': invoice.get_settlement_type_display(),
                    'created_by': invoice.created_by.get_display_name() if invoice.created_by else '-',
                    'price': invoice.sale_price,
                })
        
        if report.invoice_type in ['purchase', 'all']:
            for invoice in purchase_query.select_related('vendor', 'created_by'):
                service_obj = self.get_service_object(invoice.service_id, invoice.service_category)
                invoices.append({
                    'type': _('خرید'),
                    'invoice_number': invoice.invoice_number,
                    'invoice_date': invoice.invoice_date,
                    'customer_first_name': invoice.vendor.first_name,
                    'customer_last_name': invoice.vendor.last_name,
                    'service_category': invoice.get_service_category_display(),
                    'service_name': service_obj.name if service_obj else (invoice.other_service_title or _('نامشخص')),
                    'settlement_type': invoice.get_settlement_type_display(),
                    'created_by': invoice.created_by.get_display_name() if invoice.created_by else '-',
                    'price': invoice.purchase_price,
                })
        
        invoices.sort(key=lambda x: x['invoice_date'], reverse=True)
        
        total_price = sum(inv['price'] for inv in invoices)
        
        context = {
            'report': report,
            'invoices': invoices,
            'total_count': len(invoices),
            'total_price': total_price,
            'title': _('گزارش مشتری'),
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request),
        }
        
        response = TemplateResponse(
            request,
            'admin/reports/customer_report_detail.html',
            context,
        )
        response['Content-Type'] = 'text/html; charset=utf-8'
        return response
    
    def generate_report_form(self, request):
        from persons.models import Person
        
        if request.method == 'POST':
            customer_id = request.POST.get('customer')
            service_category = request.POST.get('service_category')
            service_id = request.POST.get('service_id')
            invoice_type = request.POST.get('invoice_type', 'all')
            settlement_type = request.POST.get('settlement_type', 'all')
            single_date = request.POST.get('single_date')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            created_by_id = request.POST.get('created_by')
            
            try:
                customer = None
                if customer_id:
                    customer = Person.objects.get(pk=customer_id)
                
                created_by = None
                if created_by_id:
                    created_by = CustomUser.objects.get(pk=created_by_id)
                
                report_data = {
                    'customer': customer,
                    'service_category': service_category or '',
                    'service_id': service_id if service_id else None,
                    'invoice_type': invoice_type,
                    'settlement_type': settlement_type,
                    'single_date': single_date if single_date else None,
                    'start_date': start_date if start_date else None,
                    'end_date': end_date if end_date else None,
                    'created_by': created_by,
                    'generated_by': request.user,
                }
                
                report = CustomerReport.objects.create(**report_data)
                report_url = reverse('admin:reports_customerreport_view_customer_report', args=[report.id])
                return redirect(report_url)
            except Exception as e:
                pass
        
        customers = Person.objects.filter(is_active=True).order_by('first_name', 'last_name')
        users = CustomUser.objects.filter(is_active=True).order_by('first_name', 'last_name')
        service_categories = CustomerReport.SERVICE_CATEGORY_CHOICES
        
        context = {
            'customers': customers,
            'users': users,
            'service_categories': service_categories,
            'title': _('تولید گزارش مشتری'),
            'opts': self.model._meta,
        }
        
        response = TemplateResponse(
            request,
            'admin/reports/generate_customer_report_form.html',
            context,
        )
        response['Content-Type'] = 'text/html; charset=utf-8'
        return response
    
    def api_services_by_category(self, request):
        import json
        from django.http import JsonResponse
        from services.models import (
            CommercialService, RegistrationService, LegalService,
            LeasingService, LoanService
        )
        
        category = request.GET.get('category')
        
        model_map = {
            'commercial': CommercialService,
            'registration': RegistrationService,
            'legal': LegalService,
            'leasing': LeasingService,
            'loan': LoanService,
        }
        
        model = model_map.get(category)
        if model:
            services = model.objects.filter(is_active=True).values('id', 'name')
            return JsonResponse({'services': list(services)})
        
        return JsonResponse({'services': []})
    
    def get_service_object(self, service_id, service_type):
        from services.models import (
            CommercialService, RegistrationService, LegalService,
            LeasingService, LoanService
        )
        
        if not service_id or not service_type:
            return None
        
        model_map = {
            'commercial': CommercialService,
            'registration': RegistrationService,
            'legal': LegalService,
            'leasing': LeasingService,
            'loan': LoanService,
        }
        
        model = model_map.get(service_type)
        if model:
            try:
                return model.objects.get(id=service_id)
            except model.DoesNotExist:
                return None
        return None


admin.site.register(EmployeeReport, EmployeeReportAdmin)
admin.site.register(FinancialReport, FinancialReportAdmin)
admin.site.register(CustomerReport, CustomerReportAdmin)
