from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        user = self.request.user
        
        if user.is_superuser or user.is_staff or user.role == 'admin':
            if user.role == 'admin' and not user.is_staff:
                user.is_staff = True
                user.save(update_fields=['is_staff'])
            return reverse_lazy('admin:index')
        else:
            return reverse_lazy('employee-admin:index')
