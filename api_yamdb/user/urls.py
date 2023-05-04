from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'api/v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/signup/', views.signup, name='signup')
]
