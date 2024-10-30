from rest_framework import mixins, permissions, viewsets

from api.permissions import AdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    # permission_classes = (AdminOrReadOnly,)
    permission_classes = (permissions.AllowAny,)
    search_fields = ('name',)
    lookup_field = 'slug'
