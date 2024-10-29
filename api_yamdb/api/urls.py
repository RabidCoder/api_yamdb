from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet


PREFIX_API_V1 = 'v1'

router_v1 = DefaultRouter()
router_v1.register(f'{PREFIX_API_V1}/categories', CategoryViewSet)
router_v1.register(f'{PREFIX_API_V1}/genres', GenreViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
