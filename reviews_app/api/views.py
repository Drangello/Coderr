"""API views for listing, creating, and managing reviews."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter

from reviews_app.api.filters import ReviewFilter
from reviews_app.api.permissions import IsCustomerUser, IsReviewOwnerOrReadOnly
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for review listing, creation, update, and deletion."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']

    def get_permissions(self):
        """Return permissions based on the review action."""
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated(), IsReviewOwnerOrReadOnly()]
