"""
Auth Middleware — Shivank Kirana Store
JWT token verification for API endpoints
"""
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthMiddleware:
    """
    Optional JWT middleware for API routes.
    Non-API routes pass through normally (use Django session auth).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply JWT auth to /api/* routes
        if request.path.startswith('/api/'):
            token = self._extract_token(request)
            if token:
                user = self._authenticate_token(token)
                if user:
                    request.user = user

        return self.get_response(request)

    def _extract_token(self, request) -> str | None:
        """Extract Bearer token from Authorization header."""
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None

    def _authenticate_token(self, token: str):
        """Decode JWT and return user."""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            user_id = payload.get('user_id')
            return User.objects.get(id=user_id, is_active=True)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return None
