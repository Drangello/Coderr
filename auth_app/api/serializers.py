from django.contrib.auth.models import User
from rest_framework import serializers
from profile_app.models import Profile

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=Profile.UserType.choices, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # Check if email is already used
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError({"email": "Email is already in use."})
            
        return data

    def create(self, validated_data):
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Profile is created automatically via signal, but we update the type if needed.
        # Actually, let's create it explicitly or via signal. Let's do it explicitly in service or view.
        # Wait, if we use a signal, it creates a profile with default type. Let's do it here explicitly to avoid signal complexities.
        Profile.objects.create(user=user, type=user_type)
        
        return user
