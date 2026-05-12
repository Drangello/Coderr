from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Avg
from profile_app.models import Profile
from offers_app.models import Offer
from reviews_app.models import Review

class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            average_rating = round(average_rating, 1)
        else:
            average_rating = 0.0
            
        business_profile_count = Profile.objects.filter(type=Profile.UserType.BUSINESS).count()
        offer_count = Offer.objects.count()
        
        return Response({
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        })
