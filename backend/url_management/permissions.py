from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Allows editing/deleting an object only if the user is the owner.
    """
    def has_object_permission(self, request, view, obj):
        # For safe methods (GET, HEAD, OPTIONS) allow access
        if request.method in SAFE_METHODS:
            return True
        # For changes - check if the user is the owner of the object
        return obj.owner == request.user
