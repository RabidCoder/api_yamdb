from rest_framework import mixins, viewsets
from rest_framework.response import Response

from api.permissions import CustomPermission


class BaseMixin(
    mixins.RetrieveModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Base mixin that provides CRUD operations for a model.

    Combines the functionalities of Retrieve, List, Create, and Destroy
    mixins and applies custom permissions defined in CustomPermission.
    """

    permission_classes = (CustomPermission,)


class NoUpdateMixin(BaseMixin):
    """
    Mixin to disable update operations.

    Inherits from BaseMixin but overrides the update method to prevent
    any updates to the resource. Returns a 405 Method Not Allowed status.
    """

    search_fields = ('name',)
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        """Returns a 405 response for update requests."""
        return Response({'detail': 'Update methods are not allowed.'}, status=405)


class PatchOnlyMixin(BaseMixin):
    """
    Mixin that allows only PATCH requests for updates.

    Inherits from BaseMixin and overrides the update method to
    restrict the use of PUT requests, allowing only PATCH requests
    for updates.
    """

    def update(self, request, *args, **kwargs):
        """Disallows PUT requests and allows only PATCH requests."""
        if request.method == 'PUT':
            return Response({'detail': 'Method "PUT" is not allowed.'}, status=405)
        return super().update(request, *args, **kwargs)
