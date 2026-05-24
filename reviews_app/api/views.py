from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter

from reviews_app.api.filters import ReviewFilter
from reviews_app.api.permissions import IsCustomerUser, IsReviewOwnerOrReadOnly
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated(), IsReviewOwnerOrReadOnly()]
