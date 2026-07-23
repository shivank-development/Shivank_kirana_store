from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from apps.accounts.serializers import RegisterSerializer, UserSerializer

User = get_user_model()

class RegisterAPIView(generics.CreateAPIView):
    """
    API endpoint to register a new user.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
