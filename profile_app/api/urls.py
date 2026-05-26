"""URL routes for profile-related API endpoints."""

from django.urls import path

from profile_app.api.views import (
    BusinessProfileListView,
    CustomerProfileListView,
    ProfileDetailView
)

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path(
        'profiles/business/',
        BusinessProfileListView.as_view(),
        name='business-profiles'
    ),
    path(
        'profiles/customer/',
        CustomerProfileListView.as_view(),
        name='customer-profiles'
    ),
]
