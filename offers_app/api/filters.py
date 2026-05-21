from django.db.models import Min
from django_filters import rest_framework as filters

from offers_app.models import Offer


class OfferFilter(filters.FilterSet):
    creator_id = filters.NumberFilter(field_name='user_id')
    min_price = filters.NumberFilter(method='filter_min_price')
    max_delivery_time = filters.NumberFilter(method='filter_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']

    def filter_min_price(self, queryset, name, value):
        return queryset.annotate(
            min_price_val=Min('details__price')
        ).filter(min_price_val__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        return queryset.annotate(
            min_delivery=Min('details__delivery_time_in_days')
        ).filter(min_delivery__lte=value)
