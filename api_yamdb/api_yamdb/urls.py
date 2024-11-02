from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from users.views import get_token, signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', signup, name='signup'),
    path('api/v1/auth/token/', get_token, name='get_token'),
    path('api/v1/users/', include('users.urls')),
    path('api/', include('api.urls')),
]
