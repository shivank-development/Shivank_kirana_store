"""
Standardized API Response Format — Shivank Kirana Store
"""
from django.http import JsonResponse


def success_response(data=None, message="Success", status=200):
    """Standard success response."""
    return JsonResponse({
        'success': True,
        'message': message,
        'data': data or {},
    }, status=status)


def error_response(message="Error", errors=None, status=400):
    """Standard error response."""
    return JsonResponse({
        'success': False,
        'message': message,
        'errors': errors or {},
    }, status=status)


def not_found_response(message="Not found"):
    """404 response."""
    return error_response(message=message, status=404)


def unauthorized_response(message="Unauthorized"):
    """401 response."""
    return error_response(message=message, status=401)


def paginated_response(queryset, page, per_page, serializer_fn):
    """Paginated list response."""
    from utilities.paginator import paginate_queryset
    page_obj, total = paginate_queryset(queryset, page, per_page)
    return success_response(data={
        'results': serializer_fn(page_obj),
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': -(-total // per_page),  # ceil division
    })
