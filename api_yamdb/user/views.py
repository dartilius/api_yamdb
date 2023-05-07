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
from .serializers import UserSerializer, ConfirmationSerializer, MeSerializer
import random


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
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
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
    code = random.randint(10000, 99999)
    if serializer.is_valid():
        if request.data['username'] == 'me':
            return Response(
                {'message': 'Username "me" недопустим.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        User.objects.create(
            username=request.data['username'],
            email=request.data['email'],
            confirmation_code=code
        )
    if 'username' not in request.data or 'email' not in request.data:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    elif not User.objects.filter(
            username=request.data['username'],
            email=request.data['email']
    ).count():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        user = User.objects.get(
            username=request.data['username'],
            email=request.data['email']
        )
        user.confirmation_code = code
        user.save()

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
    if ('username' not in request.data
            or 'confirmation_code' not in request.data):
        return Response(
            {'message': 'В запросе должны быть '
                        'поля username и confirmation_code'},
            status=status.HTTP_400_BAD_REQUEST
        )
    username = request.data.get('username')
    code = request.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if user.confirmation_code == code:
        return Response(
            {'Token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Неправильный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )
