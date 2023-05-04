from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """Пользователь."""

    username_validator = UnicodeUsernameValidator()

    ROLES = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    role = models.CharField(
        max_length=31,
        verbose_name='Роль',
        choices=ROLES,
        default='user'
    )
