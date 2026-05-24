from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg

from reviews_app.models import Review
from profile_app.models import Profile
from offers_app.models import Offer

class BaseInfoView(APIView):
    """Return basic aggregated information about the platform.

    No authentication required.
    """

    def get(self, request, *args, **kwargs):
        review_count = Review.objects.count()
        avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        # round to one decimal place
        avg_rating = round(avg_rating, 1)
        business_profile_count = Profile.objects.filter(type=Profile.UserType.BUSINESS).count()
        offer_count = Offer.objects.count()
        data = {
            "review_count": review_count,
            "average_rating": avg_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data)
