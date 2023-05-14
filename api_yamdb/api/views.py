from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.filters import FilterTitle
from user.permissions import (
    IsAuthorOrModeratorOrReadOnly,
    IsAdminOrSuperUserOrReadOnly
)
from reviews.models import Genre, Category, Title, Review
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleSerializer,
    TitleCreateSerializer,
    ReviewSerializer,
    CommentSerializer
)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для CreateListDestroyGenericSerializer."""
    pass


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для GenreSerializer."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    filterset_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для CategorySerializer."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    filterset_fields = ('name', 'slug')
    lookup_field = 'slug'
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для TitleSerializer."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = FilterTitle
    search_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            queryset = (Title.objects.prefetch_related('reviews').all().
                        annotate(rating=Avg('reviews__score')).
                        order_by('name'))
            return queryset
        return Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для ReviewSerializer."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorOrModeratorOrReadOnly, IsAuthenticatedOrReadOnly,
    )

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для CommentSerializer."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrModeratorOrReadOnly, IsAuthenticatedOrReadOnly,
    )

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
