"""Serializers for authentication-related API payloads."""

from django.contrib.auth.models import User

from rest_framework import serializers

from profile_app.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration requests."""

    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=Profile.UserType.choices, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """Validate that the password repetition matches and the email is unique."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})
        return data

    def create(self, validated_data):
        """Create a new user and associated profile from validated registration data."""
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')
        user = self._create_user(validated_data)
        Profile.objects.create(user=user, type=user_type)
        return user

    def _create_user(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
