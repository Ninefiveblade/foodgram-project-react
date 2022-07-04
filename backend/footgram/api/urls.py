"""Роутинг приложения API."""
from django.urls import include, path
from djoser.views import UserViewSet, TokenDestroyView, TokenCreateView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'^users', UserViewSet, basename='users')
router.register(r'^tags', views.TagViewSet, basename='tags')
router.register(r'^recipes', views.RecipeViewSet, basename='recipes')
router.register(r'^ingredients', views.IngredientViewset, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('users/set_password/', UserViewSet.as_view({"post": "reset_password"}), name="reset_password"),
    path('auth/token/login/', TokenCreateView.as_view(), name="login"),
    path('auth/token/logout/', TokenDestroyView.as_view(), name="logout")
]
