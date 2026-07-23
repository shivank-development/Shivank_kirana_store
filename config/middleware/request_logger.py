"""Request/Response logging middleware."""
import logging
import time

logger = logging.getLogger('apps')


class RequestLoggerMiddleware:
    """Log all incoming requests with timing."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        logger.debug(
            f'{request.method} {request.path} → {response.status_code} ({duration:.3f}s)'
        )
        return response
