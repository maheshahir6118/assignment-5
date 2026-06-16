from rest_framework.permissions import BasePermission

class IsPremiumUser(BasePermission):
    """
    Custom permission class that only allows premium users to access the endpoint.
    Requires:
    1. User is authenticated.
    2. User profile exists and has is_premium = True.
    """
    def has_permission(self, request, view):
        # 1. User must be authenticated
        if not (request.user and request.user.is_authenticated):
            return False
        
        # 2. User must have a premium profile flag
        try:
            return request.user.profile.is_premium
        except AttributeError:
            return False
