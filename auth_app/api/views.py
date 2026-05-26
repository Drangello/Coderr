"""Authentication API views for registration and login.

This module exposes two unauthenticated endpoints: registration and login.
The registration endpoint creates a new user and returns an auth token.
The login endpoint validates credentials and returns an existing token.
"""

from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.serializers import RegistrationSerializer


def token_response(user, response_status):
    """Build a standard token response payload for authenticated users."""
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "username": user.username,
        "email": user.email,
        "user_id": user.id
    }, status=response_status)


class RegistrationView(generics.CreateAPIView):
    """API endpoint for user registration.

    Accepts username, email, password, repeated_password, and type.
    Creates a new user, creates an associated profile, and returns a token.
    """

    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return token_response(user, status.HTTP_201_CREATED)


class CustomLoginView(APIView):
    """API endpoint for user login and token retrieval."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Authenticate the user and return an auth token on success."""
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return self._error_response("Please provide both username and password.")

        user = authenticate(username=username, password=password)
        if not user:
            return self._error_response("Invalid credentials.")
        return token_response(user, status.HTTP_200_OK)

    def _error_response(self, message):
        """Return a standardized validation error response."""
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
