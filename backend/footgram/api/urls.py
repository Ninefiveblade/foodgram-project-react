"""Rout module for api app."""
from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"^users", views.FoodgramUserViewSet, basename="users")
router.register(r"^tags", views.TagViewSet, basename="tags")
router.register(r"^recipes", views.RecipeViewSet, basename="recipes")
router.register(
    r"^ingredients", views.IngredientViewset, basename="ingredients"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "users/change-password/",
        UserViewSet.as_view({"post": "reset_password"}),
        name="reset_password"
    ),
    path("auth/token/login/", TokenCreateView.as_view(), name="login"),
    path("auth/token/logout/", TokenDestroyView.as_view(), name="logout"),
]
