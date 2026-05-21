from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.api.serializers import RegistrationSerializer


def token_response(user, response_status):
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "username": user.username,
        "email": user.email,
        "user_id": user.id
    }, status=response_status)


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return token_response(user, status.HTTP_201_CREATED)


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return self._error_response("Please provide both username and password.")

        user = authenticate(username=username, password=password)
        if not user:
            return self._error_response("Invalid credentials.")
        return token_response(user, status.HTTP_200_OK)

    def _error_response(self, message):
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
