from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    """Права доступа администратора и суперпользователя."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == 'admin' or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (
                request.user.role == 'admin' or request.user.is_superuser)
        )


class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    """Права доступа для автора."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (
                    request.user == obj.author
                    or request.user.role == 'moderator'
                    or request.user.role == 'admin'
                    or request.user.is_superuser
                )
                )


class IsAdminOrSuperUserOrReadOnly(permissions.BasePermission):
    """Права доступа администратора и суперпользователя."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser)
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser)
                )
