"""Permission classes for the offers API."""

from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """Permission allowing only business profile users to create offers."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, 'profile', None)
        return profile and profile.type == 'business'


class IsOfferOwnerOrReadOnly(permissions.BasePermission):
    """Permission that allows read-only access for everyone but edits only for the owner."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
