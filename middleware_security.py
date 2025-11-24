"""
Custom security middleware and decorators for Phonix Dashboard
"""

import logging
import hashlib
from functools import wraps
from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.conf import settings
from decouple import config

logger = logging.getLogger(__name__)


class RateLimitMiddleware(MiddlewareMixin):
    """
    Rate limiting middleware to prevent abuse.
    Uses cache backend to track requests.
    """
    
    def get_client_ip(self, request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def process_request(self, request):
        """Check rate limits on incoming request"""
        
        if request.path.startswith('/admin/'):
            rate_limit = 10
            window = 60
        elif request.path.startswith('/api/'):
            rate_limit = 30
            window = 60
        else:
            rate_limit = 60
            window = 60
        
        client_ip = self.get_client_ip(request)
        cache_key = f"rate_limit:{client_ip}"
        
        request_count = cache.get(cache_key, 0)
        
        if request_count >= rate_limit:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JsonResponse(
                {'error': 'Too many requests. Please try again later.'},
                status=429
            )
        
        cache.set(cache_key, request_count + 1, window)
        
        return None


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add additional security headers to responses
    """
    
    def process_response(self, request, response):
        """Add security headers to response"""
        
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        return response


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Log all requests for security auditing
    """
    
    def process_request(self, request):
        """Log incoming request"""
        if request.method in ['POST', 'PUT', 'DELETE']:
            logger.info(
                f"[{request.method}] {request.path} - "
                f"User: {request.user} - "
                f"IP: {self.get_client_ip(request)}"
            )
        return None
    
    def get_client_ip(self, request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


def rate_limit(requests_per_minute=60):
    """
    Decorator to rate limit individual views
    Usage: @rate_limit(requests_per_minute=10)
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
            cache_key = f"view_rate_limit:{view_func.__name__}:{client_ip}"
            
            request_count = cache.get(cache_key, 0)
            
            if request_count >= requests_per_minute:
                logger.warning(
                    f"View rate limit exceeded for {view_func.__name__} - IP: {client_ip}"
                )
                return JsonResponse(
                    {'error': 'Too many requests. Please try again later.'},
                    status=429
                )
            
            cache.set(cache_key, request_count + 1, 60)
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def api_key_required(view_func):
    """
    Decorator to require API key authentication
    Usage: @api_key_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        api_key = request.META.get('HTTP_X_API_KEY') or request.GET.get('api_key')
        
        if not api_key:
            logger.warning(f"API request without key: {request.path}")
            return JsonResponse(
                {'error': 'API key is required'},
                status=401
            )
        
        valid_api_key = config('API_KEY', default='')
        
        if not valid_api_key or api_key != valid_api_key:
            logger.warning(f"Invalid API key attempt: {request.path}")
            return JsonResponse(
                {'error': 'Invalid API key'},
                status=403
            )
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def require_https(view_func):
    """
    Decorator to require HTTPS connections
    Usage: @require_https
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not settings.DEBUG and not request.is_secure():
            logger.warning(f"Non-HTTPS access attempt: {request.path}")
            return JsonResponse(
                {'error': 'HTTPS is required'},
                status=403
            )
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def audit_log(action_name):
    """
    Decorator to log sensitive actions
    Usage: @audit_log("user_login")
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
            user = request.user if request.user.is_authenticated else 'Anonymous'
            
            logger.warning(
                f"[AUDIT] {action_name} - User: {user} - IP: {client_ip} - Path: {request.path}"
            )
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
