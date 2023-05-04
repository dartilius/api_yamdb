from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, get_token

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'api/v1/auth/token/',
        get_token,
        name='token_obtain_pair'
    ),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/signup/', views.signup, name='signup')
]
