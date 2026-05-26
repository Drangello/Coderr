"""Filters for review list queries."""

from django_filters import rest_framework as filters
from reviews_app.models import Review

class ReviewFilter(filters.FilterSet):
    """FilterSet that exposes business_user_id and reviewer_id filters."""
    business_user_id = filters.NumberFilter(field_name='business_user')
    reviewer_id = filters.NumberFilter(field_name='reviewer')

    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']
