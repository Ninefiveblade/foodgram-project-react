"""Permissions module for api app."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class RecipeIsStaffOrOwner(BasePermission):
    """Custom Permission for RecipeViewSet
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            or request.method in SAFE_METHODS
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
    """Custom permission for User/Follow"""

    def has_permission(self, request, view):
        if view.action == "list":
            return (request.user.is_authenticated or request.user)
        return request.user.is_authenticated
