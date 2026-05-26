"""Permissions for review endpoints."""

from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Only allow customers to create new reviews."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, 'profile', None)
        return profile and profile.type == 'customer'


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """Allow read access to all authenticated users and write access to the review owner."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user
