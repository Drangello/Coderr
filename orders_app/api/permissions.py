from rest_framework import permissions

class IsCustomerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, 'profile', None) and request.user.profile.type == 'customer'

class IsBusinessUserAndOrderParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if getattr(request.user, 'profile', None) and request.user.profile.type == 'business':
            return obj.business_user == request.user
        return False
