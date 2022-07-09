"""Views module for api app."""
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet

from .mixins import (
    CustomListRetriveViewSet, CustomCreateDestroyViewSet, RecipeMixin
)
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
        serializer = serializers.RecipeSerializer(
            instance, data=request.data, partial=True
        )
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
    serializer_class = serializers.FoodgramFollowSerializer
    queryset = Follow.objects.all()

    def perform_create(self, serializer):
        author = models.FoodgramUser.objects.get(id=self.kwargs.get('id'))
        serializer.save(
            author=author,
            user=self.request.user
        )

    @action(methods=['delete'], detail=False)
    def delete(self, request, id):
        try:
            models.FoodgramUser.objects.get(id=id)
            Follow.objects.get(author_id=id, user_id=request.user).delete()
            return Response(status=204)
        except Follow.DoesNotExist:
            return Response(
                {"errors": "Вы не подписаны на данного автора."}, status=401
            )
        except models.FoodgramUser.DoesNotExist:
            return Response({"detail": "Страница не найдена."}, status=404)


class FoodgramUserViewSet(UserViewSet):
    def create(self, request, *args, **kwargs):
        serializer = serializers.FoodramRegisterInSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            output_serializer = serializers.FoodgramRegisterOutSerializer(user)
            return Response(output_serializer.data)
        else:
            return Response(serializer.errors, 400)

    @action(methods=('GET',), detail=False)
    def subscriptions(self, request):
        follows = Follow.objects.filter(user=request.user)
        list_of_authors = []
        for follow in follows:
            list_of_authors.append(self.serializer_class(follow.author).data)
        return Response(list_of_authors, 200)
