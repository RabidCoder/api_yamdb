from rest_framework import permissions

from constants import ADMIN


class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == ADMIN
                or request.user.is_superuser)
