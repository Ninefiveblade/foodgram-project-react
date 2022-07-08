"""Views module for api app."""
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken import views

from .mixins import CustomListRetriveViewSet, CustomCreateDestroyViewSet, RecipeMixin
from . import serializers
from cooking import models
from users.models import Follow


class RecipeViewSet(RecipeMixin):
    queryset = models.Recipe.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = serializers.RecipeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            recipe = serializer.save(author=self.request.user)
            output_serializer = serializers.RecipeOutSerializer(recipe)
            return Response(output_serializer.data)
        else:
            return Response(serializer.errors, 400)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.RecipeSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            recipe = serializer.save()
            output_serializer = serializers.RecipeOutSerializer(recipe)
            return Response(output_serializer.data)
        else:
            return Response(serializer.errors, 400)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return serializers.RecipeOutSerializer
        if self.action in ('partial_update',):
            return serializers.RecipeOutSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )


class TagViewSet(CustomListRetriveViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewset(CustomListRetriveViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class FollowViewSet(CustomCreateDestroyViewSet):
    queryset = Follow.objects.all()
    serializer_class = serializers.FoodgramFollowSerializer

    def perform_create(self, serializer):
        author = models.FoodgramUser.objects.get(id=self.kwargs.get('id'))
        serializer.save(
            author=author,
            user=self.request.user
        )
