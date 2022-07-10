"""Permissions module for api app."""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrOwner(BasePermission):
    """Пермишен доступа персонала и пользователя.
    Переопределенные методы:
    Общий -has_permission
    Объектный - has_object_permission.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or (
                request.user.is_authenticated
                and (
                    request.user.is_admin
                    or request.user.is_moderator
                )
            )
            or request.user.is_superuser
        )
