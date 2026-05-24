from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from reviews_app.models import Review
from profile_app.models import Profile
from offers_app.models import Offer

class BaseInfoView(APIView):
    """Aggregated platform statistics for the front‑end.

    Returns:
        {
            "review_count": int,
            "average_rating": float,  # rounded to one decimal place
            "business_profile_count": int,
            "offer_count": int,
        }
    """
    permission_classes = []  # public endpoint, no authentication required

    def get(self, request, *args, **kwargs):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0.0
        # round to one decimal place as required
        average_rating = round(average_rating, 1)
        business_profile_count = Profile.objects.filter(type=Profile.UserType.BUSINESS).count()
        offer_count = Offer.objects.count()
        return Response({
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        })
