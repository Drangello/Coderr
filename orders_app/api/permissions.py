"""Permission classes used by the order API."""

from rest_framework import permissions


class IsCustomerUser(permissions.BasePermission):
    """Allow access only to users with a customer profile."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, 'profile', None)
        return profile and profile.type == 'customer'


class IsBusinessUserAndOrderParticipant(permissions.BasePermission):
    """Allow business users to update orders they own."""

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        profile = getattr(request.user, 'profile', None)
        if profile and profile.type == 'business':
            return obj.business_user == request.user
        return False
