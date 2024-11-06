from rest_framework import permissions

from users.constants import ADMIN, MODERATOR


class AdminPermission(permissions.BasePermission):
    """
    Custom permission that allows safe methods for all users
    and restricts other methods to authenticated admins only.
    """

    def has_permission(self, request, view):
        # Allow safe methods for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow other methods only for authenticated users with 'admin' role
        return request.user.is_authenticated and request.user.role == ADMIN


class CustomPermission(permissions.BasePermission):
    """
    Custom permission that allows safe methods for all users
    and restricts other methods to authenticated users.
    Allows object modification for the object author, moderators, and admins.
    """

    def has_permission(self, request, view):
        # Allow safe methods for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow other methods only for authenticated users
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for unauthenticated users
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        # Allow safe methods for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow modifications for object author, moderators, and admins
        return (
            obj.author == request.user
            or request.user.role in (ADMIN, MODERATOR)
        )
