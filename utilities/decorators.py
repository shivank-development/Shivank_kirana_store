"""
Custom Decorators — Shivank Kirana Store
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Restrict view to admin users only."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth:login')
        if not (request.user.is_staff or request.user.is_superuser or 
                getattr(request.user, 'role', '') == 'admin'):
            messages.error(request, 'Admin access required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def delivery_boy_required(view_func):
    """Restrict view to delivery boys only."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth:login')
        if getattr(request.user, 'role', '') != 'delivery':
            messages.error(request, 'Delivery boy access required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_required_ajax(view_func):
    """Return JSON 401 for unauthenticated AJAX requests."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from utilities.response import unauthorized_response
            return unauthorized_response('Please login to continue.')
        return view_func(request, *args, **kwargs)
    return wrapper
