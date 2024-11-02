from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """
    Permission class checks whether the request user is admin.
    If not, he/she gets a read only permission.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin'
        )


class AuthorOrReadOnly(permissions.BasePermission):
    """Permission class to restrict content modification and deletion."""

    def has_permission(self, request, view):
        """Allow read permissions for unauthenticated users."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Allow modification and deletion for the author,
        moderators, and admins."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role in ('moderator', 'admin', 'author')
        )
