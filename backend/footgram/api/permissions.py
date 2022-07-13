"""Permissions module for api app."""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class RecipeIsStaffOrOwner(BasePermission):
    """Пермишен доступа персонала и пользователя.
    Переопределенные методы:
    Общий -has_permission
    Объектный - has_object_permission.
    """
    def has_permission(self, request, view):
        if view.action == 'download_shopping_cart':
            return request.user.is_authenticated
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or (request.user.is_admin
                or request.user.is_superuser
                )
        )


class UserIsAuthentificated(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return (request.user.is_authenticated or request.user)
        return request.user.is_authenticated
