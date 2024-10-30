from rest_framework import mixins, viewsets

from api.permissions import AdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Source class to inherit Category and Genre viewsets from."""

    permission_classes = (AdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
