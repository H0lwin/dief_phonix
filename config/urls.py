from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from accounts.admin import employee_admin_site

urlpatterns = [
    path('', RedirectView.as_view(url='accounts/login/', permanent=False), name='index'),
    path('admin/', admin.site.urls),
    path('employee-admin/', employee_admin_site.urls),
    path('accounts/', include('accounts.urls')),
    path('persons/', include('persons.urls')),
    path('reports/', include('reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
