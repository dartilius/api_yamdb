from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для пользователей."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class ConfirmationSerializer(serializers.Serializer):
    """Сериалайзер для регистрации пользователей."""

    username = serializers.RegexField(regex=r'^[\w.@+-]', max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate(self, data):
        if User.objects.filter(
            username=data['username'],
            email=data['email']
        ).exists():
            return data
        if User.objects.filter(
                username=data['username']
        ).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует.'
            )
        if User.objects.filter(
                email=data['email']
        ).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return data

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('username не может быть "me"')
        return value


class MeSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения данных пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class TokenSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения токена."""

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        valid_code = default_token_generator.check_token(
            user,
            data['confirmaion_code']
        )
        if not valid_code:
            raise serializers.ValidationError(
                'Неправильный код подтверждения.'
            )
        return data
