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


class ConfirmationSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователей."""

    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )


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
