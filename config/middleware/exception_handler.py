"""
Global Exception Handler Middleware — Shivank Kirana Store
Catches unhandled exceptions and returns clean JSON response
"""
import traceback
import logging
from django.http import JsonResponse

logger = logging.getLogger('django')


class ExceptionHandlerMiddleware:
    """Catch all unhandled exceptions and return clean response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        """Called when an unhandled exception occurs in a view."""
        logger.error(
            f"Unhandled exception on {request.path}: {exception}",
            exc_info=True
        )

        # For AJAX requests — return JSON error
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'An unexpected error occurred. Please try again.',
                'error': str(exception) if __debug__ else 'Internal server error'
            }, status=500)

        # For regular requests — let Django handle it (shows 500 page)
        return None
