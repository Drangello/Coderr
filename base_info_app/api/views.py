from django.db.models import Avg

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from profile_app.models import Profile
from reviews_app.models import Review


class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response(get_base_info())


def get_base_info():
    return {
        "review_count": Review.objects.count(),
        "average_rating": get_average_rating(),
        "business_profile_count": get_business_profile_count(),
        "offer_count": Offer.objects.count()
    }


def get_average_rating():
    average_rating = Review.objects.aggregate(Avg('rating'))['rating__avg']
    return round(average_rating, 1) if average_rating is not None else 0.0


def get_business_profile_count():
    return Profile.objects.filter(type=Profile.UserType.BUSINESS).count()
