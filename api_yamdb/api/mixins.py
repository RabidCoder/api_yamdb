from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from api.permissions import AdminPermission, CustomPermission


class BaseModelViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Base viewset that provides common functionality
    for category and genre viewsets.
    """

    permission_classes = (AdminPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class NonPutModelViewSet(viewsets.ModelViewSet):
    """
    A base viewset that extends ModelViewSet to customize the update method.
    """

    permission_classes = (CustomPermission,)

    def update(self, request, *args, **kwargs):
        """
        Override the update method to block PUT requests.

        Returns a 405 Method Not Allowed response for PUT requests.
        """
        if request.method == 'PUT':
            return Response(
                {'detail': 'Method "PUT" is not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)
