from rest_framework.routers import SimpleRouter

from .views import (GenreViewSet,
                    CategoryViewSet,
                    TitleViewSet)

router_v1 = SimpleRouter()

router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)


