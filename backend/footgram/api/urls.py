"""Роутинг приложения API."""
from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'^users', UserViewSet, basename='users')
router.register(r'^genres', views.TagViewSet, basename='tags')
router.register(r'^recipes', views.RecipeViewSet, basename='recipes')
router.register(r'^ingredients', views.IngredientViewset, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('users/set_password/', UserViewSet.as_view({"post": "reset_password"}), name="reset_password"),
    path('auth/token/login/', TokenObtainPairView.as_view(), name="login"),
    path('auth/token/logout/',  TokenObtainPairView.as_view(), name="logout")
]
