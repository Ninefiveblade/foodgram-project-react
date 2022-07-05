from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken import views

from .mixins import CustomViewSet
from . import serializers
from cooking import models


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )


class TagViewSet(CustomViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewset(CustomViewSet):
    queryset = models.IngredientQuantity.objects.all()
    serializer_class = serializers.IngredientSerializer
