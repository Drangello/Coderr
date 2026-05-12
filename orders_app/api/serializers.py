from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import OfferDetail

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 
            'revisions', 'delivery_time_in_days', 'price', 
            'features', 'offer_type', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'customer_user', 'business_user', 'title', 
            'revisions', 'delivery_time_in_days', 'price', 
            'features', 'offer_type', 'created_at', 'updated_at'
        ]

class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    def validate_offer_detail_id(self, value):
        try:
            detail = OfferDetail.objects.get(id=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("Offer detail not found.")
        return value

    def create(self, validated_data):
        offer_detail_id = validated_data['offer_detail_id']
        detail = OfferDetail.objects.get(id=offer_detail_id)
        offer = detail.offer
        
        request = self.context.get('request')
        customer_user = request.user
        business_user = offer.user
        
        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status=Order.Status.IN_PROGRESS
        )
        return order

    def to_representation(self, instance):
        serializer = OrderSerializer(instance)
        return serializer.data
