"""URL routes for review API endpoints."""

from django.urls import path
from reviews_app.api.views import ReviewViewSet

urlpatterns = [
    path('reviews/', ReviewViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='review-list'),
    path('reviews/<int:pk>/', ReviewViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'put': 'update',
        'delete': 'destroy'
    }), name='review-detail'),
]
