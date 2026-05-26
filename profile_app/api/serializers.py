"""Serializer definitions for profile endpoint payloads."""

from rest_framework import serializers

from profile_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for reading and updating Profile objects."""

    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')
    uploaded_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at',
            'uploaded_at'
        ]
        read_only_fields = ['user', 'type', 'created_at']

    def update(self, instance, validated_data):
        """Update the Profile and its user email when provided."""
        user_data = validated_data.pop('user', {})
        if 'email' in user_data:
            instance.user.email = user_data['email']
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
