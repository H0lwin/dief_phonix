from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Q
from .models import Person, SalesInvoice
from .forms import PersonForm, SalesInvoiceForm


@require_http_methods(["GET"])
@ensure_csrf_cookie
def get_services_by_category(request):
    service_type = request.GET.get('service_type')
    if not service_type:
        return JsonResponse({'error': 'service_type is required'}, status=400)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
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
        if not model:
            return JsonResponse({'error': 'Invalid service_type'}, status=400)
        
        queryset = model.objects.filter(is_active=True)
        if request.user.role != 'admin' and not request.user.is_superuser:
            queryset = queryset.filter(created_by=request.user)
            
        if service_type == 'loan':
            services_qs = queryset.order_by('bank_name', 'plan_name')
            services = [{'id': s.id, 'name': str(s)} for s in services_qs]
        else:
            services = list(queryset.values('id', 'name').order_by('name'))
        
        return JsonResponse({
            'success': True,
            'services': services
        })
    except Exception as e:
        return JsonResponse({'error': 'Server error occurred'}, status=500)


@require_http_methods(["GET"])
@ensure_csrf_cookie
def search_persons(request):
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        queryset = Person.objects.filter(is_active=True)
        if request.user.role != 'admin' and not request.user.is_superuser:
            queryset = queryset.filter(created_by=request.user)
            
        persons = queryset.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(national_id__icontains=query) |
            Q(phone_number__icontains=query)
        ).values('id', 'first_name', 'last_name', 'national_id', 'phone_number')[:10]
        
        results = []
        for person in persons:
            results.append({
                'id': person['id'],
                'text': f"{person['first_name']} {person['last_name']} ({person['national_id']})"
            })
        
        return JsonResponse({'results': results})
    except Exception as e:
        return JsonResponse({'error': 'Server error occurred'}, status=500)
