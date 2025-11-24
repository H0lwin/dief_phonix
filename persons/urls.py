from django.urls import path
from . import views

app_name = 'persons'

urlpatterns = [
    path('api/services-by-category/', views.get_services_by_category, name='api_services_by_category'),
    path('api/search-persons/', views.search_persons, name='api_search_persons'),
]
