"""URL routes for the offer API endpoints."""

from django.urls import path
from offers_app.api.views import (
    OfferDetailViewSet,
    OfferViewSet
)

urlpatterns = [
    path('offers/', OfferViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='offer-list'),
    path('offers/<int:pk>/', OfferViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'put': 'update',
        'delete': 'destroy'
    }), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferDetailViewSet.as_view({
        'get': 'retrieve'
    }), name='offerdetail-detail'),
]
