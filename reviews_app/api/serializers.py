from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            self._validate_unique_review(data, request.user)
        return data

    def _validate_unique_review(self, data, reviewer):
        business_user = data.get('business_user')
        review_exists = Review.objects.filter(
            business_user=business_user,
            reviewer=reviewer
        ).exists()
        if review_exists:
            message = "You have already reviewed this business user."
            raise serializers.ValidationError(message)

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('business_user', None)
        return super().update(instance, validated_data)
