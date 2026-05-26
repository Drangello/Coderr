"""API views for offer listing, creation, and detail retrieval."""

from django.db.models import Min

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from offers_app.api.filters import OfferFilter
from offers_app.api.permissions import IsBusinessUser, IsOfferOwnerOrReadOnly
from offers_app.api.serializers import (
    OfferCreateUpdateSerializer,
    OfferDetailSerializer,
    OfferListSerializer
)
from offers_app.models import Offer, OfferDetail


class OfferViewSet(viewsets.ModelViewSet):
    """ViewSet for managing offers and filtering available offers."""

    queryset = Offer.objects.all()
    pagination_class = None
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def get_queryset(self):
        """Annotate offers with their minimum price and sort by update time."""
        return Offer.objects.annotate(
            min_price=Min('details__price')
        ).order_by('-updated_at')

    def get_serializer_class(self):
        """Use create/update serializer for mutating actions, list serializer otherwise."""
        if self.action in ['create', 'partial_update', 'update']:
            return OfferCreateUpdateSerializer
        return OfferListSerializer

    def get_permissions(self):
        """Return permissions depending on the action being performed."""
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        if self.action in ['partial_update', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOfferOwnerOrReadOnly()]
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class OfferDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view set for single offer detail objects."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
