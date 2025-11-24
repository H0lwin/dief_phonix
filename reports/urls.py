from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('customer-report/', views.generate_customer_report, name='customer_report_form'),
    path('customer-report/<int:pk>/', views.customer_report_detail, name='customer_report_detail'),
]
