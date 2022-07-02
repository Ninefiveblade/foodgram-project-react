"""Роутинг приложения API."""
from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'^users', views.FoodgramUserViewset, basename='users')
router.register(r'^genres', views.TagViewSet, basename='tags')
router.register(r'^recipes', views.RecipeViewSet, basename='recipes')
router.register(r'^ingredients', views.IngredientViewset, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
