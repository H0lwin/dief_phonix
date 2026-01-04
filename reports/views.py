from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date
from persons.models import SalesInvoice, PurchaseInvoice
from services.models import (
    CommercialService, RegistrationService, LegalService,
    LeasingService, LoanService
)
from .models import CustomerReport
from .forms import CustomerReportForm


def get_service_object(service_id, service_type):
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


@login_required
def generate_customer_report(request):
    if request.method == 'POST':
        form = CustomerReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            return redirect('reports:customer_report_detail', pk=report.id)
    else:
        form = CustomerReportForm()
    
    context = {
        'form': form,
        'title': 'تولید گزارش مشتری',
    }
    return render(request, 'reports/customer_report_form.html', context)


@login_required
def customer_report_detail(request, pk):
    from django.core.exceptions import PermissionDenied
    from django.shortcuts import get_object_or_404
    report = get_object_or_404(CustomerReport, id=pk)
    
    if request.user.role != 'admin' and not request.user.is_superuser and report.created_by != request.user:
        raise PermissionDenied
    
    # Build query for SalesInvoice
    sales_query = SalesInvoice.objects.all()
    purchase_query = PurchaseInvoice.objects.all()
    
    # Enforce ownership
    if request.user.role != 'admin' and not request.user.is_superuser:
        sales_query = sales_query.filter(created_by=request.user)
        purchase_query = purchase_query.filter(created_by=request.user)
    
    # Filter by customer
    if report.customer:
        sales_query = sales_query.filter(buyer=report.customer)
        purchase_query = purchase_query.filter(vendor=report.customer)
    
    # Filter by service category
    if report.service_category:
        sales_query = sales_query.filter(service_category=report.service_category)
        purchase_query = purchase_query.filter(service_category=report.service_category)
    
    # Filter by service_id
    if report.service_id:
        sales_query = sales_query.filter(service_id=report.service_id)
        purchase_query = purchase_query.filter(service_id=report.service_id)
    
    # Filter by settlement type
    if report.settlement_type != 'all':
        sales_query = sales_query.filter(settlement_type=report.settlement_type)
        purchase_query = purchase_query.filter(settlement_type=report.settlement_type)
    
    # Filter by date
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
    
    # Filter by created_by (user who registered the invoice)
    if report.filter_user:
        sales_query = sales_query.filter(created_by=report.filter_user)
        purchase_query = purchase_query.filter(created_by=report.filter_user)
    
    # Build combined results
    invoices = []
    
    if report.invoice_type in ['sales', 'all']:
        for invoice in sales_query.select_related('buyer', 'created_by'):
            service_obj = get_service_object(invoice.service_id, invoice.service_category)
            invoices.append({
                'type': 'فروش',
                'invoice_number': invoice.invoice_number,
                'invoice_date': invoice.invoice_date,
                'customer_first_name': invoice.buyer.first_name,
                'customer_last_name': invoice.buyer.last_name,
                'service_category': invoice.get_service_category_display(),
                'service_name': service_obj.name if service_obj else (invoice.other_service_title or 'نامشخص'),
                'settlement_type': invoice.get_settlement_type_display(),
                'created_by': invoice.created_by.get_display_name() if invoice.created_by else '-',
                'price': invoice.sale_price,
            })
    
    if report.invoice_type in ['purchase', 'all']:
        for invoice in purchase_query.select_related('vendor', 'created_by'):
            service_obj = get_service_object(invoice.service_id, invoice.service_category)
            invoices.append({
                'type': 'خرید',
                'invoice_number': invoice.invoice_number,
                'invoice_date': invoice.invoice_date,
                'customer_first_name': invoice.vendor.first_name,
                'customer_last_name': invoice.vendor.last_name,
                'service_category': invoice.get_service_category_display(),
                'service_name': service_obj.name if service_obj else (invoice.other_service_title or 'نامشخص'),
                'settlement_type': invoice.get_settlement_type_display(),
                'created_by': invoice.created_by.get_display_name() if invoice.created_by else '-',
                'price': invoice.purchase_price,
            })
    
    # Sort by date
    invoices.sort(key=lambda x: x['invoice_date'], reverse=True)
    
    context = {
        'report': report,
        'invoices': invoices,
        'total_count': len(invoices),
        'title': 'نتایج گزارش مشتری',
    }
    return render(request, 'reports/customer_report_detail.html', context)
