from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail

from .models import User
from .permissions import IsAdminOrSuperUser
from .serializers import (
    UserSerializer,
    ConfirmationSerializer,
    MeSerializer,
    TokenSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей."""

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('username',)
    search_fields = ('username',)
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        ['GET', 'PATCH'],
        url_path='me',
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def get_data_me(self, request):
        if request.method == 'PATCH':
            serializer = MeSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = MeSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
def signup(request):
    """Регистрация пользователей."""
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        username=request.data['username'],
        email=request.data['email']
    )
    code = default_token_generator.make_token(user)
    send_mail(
        'Confirmation Code',
        f'{code}',
        'me@example.com',
        [request.data['email']],
        fail_silently=False,
    )
    return Response(
        data=request.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get('username')
    user = get_object_or_404(User, username=username)
    return Response(
        {'Token': str(AccessToken.for_user(user))},
        status=status.HTTP_200_OK
    )
