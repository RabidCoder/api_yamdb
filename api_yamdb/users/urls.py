from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    # path('', create_user_by_admin, name='create_user_by_admin'),
    # path('me/', update_user_profile, name='update_user_profile'),
]