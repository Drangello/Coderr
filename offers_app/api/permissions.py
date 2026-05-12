from rest_framework import permissions

class IsBusinessUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, 'profile', None) and request.user.profile.type == 'business'

class IsOfferOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
