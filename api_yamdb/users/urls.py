from django.urls import path

from .views import profile, blank_url

urlpatterns = [
    path('', blank_url, name='signup'),
    path('me/', profile, name='get_token'),
]