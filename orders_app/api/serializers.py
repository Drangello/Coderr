from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.models import Order


ORDER_FIELDS = [
    'id',
    'customer_user',
    'business_user',
    'title',
    'revisions',
    'delivery_time_in_days',
    'price',
    'features',
    'offer_type',
    'status',
    'created_at',
    'updated_at'
]

ORDER_READ_ONLY_FIELDS = [
    'id',
    'customer_user',
    'business_user',
    'title',
    'revisions',
    'delivery_time_in_days',
    'price',
    'features',
    'offer_type',
    'created_at',
    'updated_at'
]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ORDER_FIELDS
        read_only_fields = ORDER_READ_ONLY_FIELDS


class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    def validate_offer_detail_id(self, value):
        if not OfferDetail.objects.filter(id=value).exists():
            raise serializers.ValidationError("Offer detail not found.")
        return value

    def create(self, validated_data):
        detail = OfferDetail.objects.get(id=validated_data['offer_detail_id'])
        return Order.objects.create(
            customer_user=self.context['request'].user,
            business_user=detail.offer.user,
            **self._order_data(detail)
        )

    def _order_data(self, detail):
        return {
            'title': detail.title,
            'revisions': detail.revisions,
            'delivery_time_in_days': detail.delivery_time_in_days,
            'price': detail.price,
            'features': detail.features,
            'offer_type': detail.offer_type,
            'status': Order.Status.IN_PROGRESS
        }

    def to_representation(self, instance):
        serializer = OrderSerializer(instance)
        return serializer.data
