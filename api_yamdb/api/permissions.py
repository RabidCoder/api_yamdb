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
