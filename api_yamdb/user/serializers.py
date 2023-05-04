from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
