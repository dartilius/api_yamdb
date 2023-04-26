from rest_framework.permissions import BasePermission, SAFE_METHODS

class ListOrAdminModeratOnly(BasePermission):
    """Редактировать список может только  администратор/суперпользователь"""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_authenticated
            and request.user.is_admin
        )
