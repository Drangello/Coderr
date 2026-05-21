from django.db import transaction

from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


OFFER_TYPES = ['basic', 'premium', 'standard']


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type'
        ]
        read_only_fields = ['id']


class OfferDetailUrlSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='offerdetail-detail')

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']


class UserDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()


class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailUrlSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]

    def get_min_price(self, obj):
        details = obj.details.all()
        return min([detail.price for detail in details]) if details else 0

    def get_min_delivery_time(self, obj):
        details = obj.details.all()
        values = [detail.delivery_time_in_days for detail in details]
        return min(values) if values else 0

    def get_user_details(self, obj):
        user = obj.user
        profile = getattr(user, 'profile', None)
        return {
            "first_name": profile.first_name if profile else "",
            "last_name": profile.last_name if profile else "",
            "username": user.username
        }


class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_details(self, details):
        if len(details) != 3:
            raise serializers.ValidationError("An offer must have exactly 3 details.")
        types = [detail.get('offer_type') for detail in details]
        if sorted(types) != OFFER_TYPES:
            message = "Offer details must include basic, standard, and premium."
            raise serializers.ValidationError(message)
        return details

    @transaction.atomic
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        validated_data['user'] = self.context['request'].user
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    @transaction.atomic
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self._update_details(instance, details_data)
        return instance

    def _update_details(self, instance, details_data):
        if not details_data:
            return
        for detail_data in details_data:
            self._update_detail(instance, detail_data)

    def _update_detail(self, instance, detail_data):
        detail = OfferDetail.objects.filter(
            offer=instance,
            offer_type=detail_data.get('offer_type')
        ).first()
        if not detail:
            return
        for attr, value in detail_data.items():
            setattr(detail, attr, value)
        detail.save()
