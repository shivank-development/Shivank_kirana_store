"""NoCache Middleware — Prevents browser BFCache/stale state on back button after form settings/actions."""

class NoCacheMiddleware:
    """Ensure dynamic & admin pages return no-cache headers so pressing Back fetches fresh page state."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        if request.user.is_authenticated or 'hard-5456' in path or request.method == 'POST':
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
