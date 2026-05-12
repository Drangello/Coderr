from rest_framework import serializers
from reviews_app.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        # We need to ensure that the reviewer hasn't already reviewed this business.
        request = self.context.get('request')
        if request and request.method == 'POST':
            business_user = data.get('business_user')
            if Review.objects.filter(business_user=business_user, reviewer=request.user).exists():
                raise serializers.ValidationError("You have already reviewed this business user.")
        return data

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)
