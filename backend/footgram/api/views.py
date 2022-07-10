"""Views module for api app."""
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from djoser.views import UserViewSet
from django.db import IntegrityError
from django.http import HttpResponse
from django.db.models import Sum

from .mixins import (
    CustomListRetriveViewSet, CustomCreateDestroyViewSet, RecipeMixin
)
from . import serializers
from cooking import models
from users.models import Follow


class RecipeViewSet(RecipeMixin):
    """Recipes viewsets."""
    queryset = models.Recipe.objects.all()

    @action(methods=["get"], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = models.IngredientQuantity.objects.filter(
            reciepe_ingredient__in=(user.shop_list_user.values('recipe_id'))
        ).values(
            "ingredient__name",
            "ingredient__measurement"
        ).annotate(amount=Sum('quantity'))
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = ["Список покупок:"]
        for ingredient in ingredients:
            shopping_list.append((
                f'{ingredient.get("ingredient__name")} '
                f'({ingredient.get("ingredient__measurement")}) — '
                f'{ingredient.get("amount")}'
            ).capitalize())
        response = HttpResponse(
            "\n".join(shopping_list), content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

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
        if self.action in ("list", "retrieve",):
            return serializers.RecipeOutSerializer
        if self.action in ("partial_update",):
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
        author = models.FoodgramUser.objects.get(id=self.kwargs.get("id"))
        serializer.save(
            author=author,
            user=self.request.user
        )

    def create(self, request, *args, **kwargs):
        try:
            author = models.FoodgramUser.objects.get(id=self.kwargs.get('id'))
            if author == request.user:
                return Response(
                    {"errors": "Вы не можете подписаться сами на себя!"},
                    400
                ) 
            Follow.objects.create(user=request.user, author=author)
            return Response(status=204)
        except IntegrityError:
            return Response({"errors": "Вы уже подписаны на этого автора!"}, 400)
        except models.FoodgramUser.DoesNotExist:
            return Response({"detail": "Страница не найдена."}, status=404)

    @action(methods=["delete"], detail=False)
    def delete(self, request, id):
        try:
            models.FoodgramUser.objects.get(id=id)
            Follow.objects.get(author_id=id, user_id=request.user).delete()
            return Response(status=204)
        except Follow.DoesNotExist:
            return Response(
                {"errors": "Вы не подписаны на данного автора."}, status=400
            )
        except models.FoodgramUser.DoesNotExist:
            return Response({"detail": "Страница не найдена."}, status=404)


class FoodgramUserViewSet(UserViewSet):
    """Вьюсет пользователей."""
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        serializer = serializers.FoodramRegisterInSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            output_serializer = serializers.FoodgramRegisterOutSerializer(user)
            return Response(output_serializer.data)
        else:
            return Response(serializer.errors, 400)

    @action(methods=("get",), detail=False)
    def subscriptions(self, request):
        follows = Follow.objects.filter(user=request.user)
        list_of_authors = []
        for follow in follows:
            list_of_authors.append(
                serializers.FoodgramFollowSerializer(follow).data
            )
        return Response(list_of_authors, 200)


class ShopingCardViewSet(CustomCreateDestroyViewSet):
    serializer_class = serializers.RecipeShortSerializer

    def create(self, request, *args, **kwargs):
        recipe = models.Recipe.objects.get(id=self.kwargs.get('recipe_id'))
        try:
            models.ShopList.objects.create(user=request.user, recipe=recipe)
        except IntegrityError:
            return Response({"errors": "Вы уже добавили товар в корзину!"}, 400)
        serializer = self.serializer_class(recipe)
        return Response(serializer.data, 201)

    @action(methods=["delete"], detail=False)
    def delete(self, request, recipe_id):
        try:
            models.Recipe.objects.get(id=recipe_id)
            models.ShopList.objects.get(recipe_id=recipe_id, user=request.user).delete()
            return Response(status=204)
        except models.Recipe.DoesNotExist:
            return Response({"errors": "Выбранного рецепта не существует!"}, 400)
        except models.ShopList.DoesNotExist:
            return Response({"detail": "Страница не найдена."}, 404)


class FavoriteRecipes(CustomCreateDestroyViewSet):
    serializer_class = serializers.RecipeShortSerializer

    def create(self, request, *args, **kwargs):
        recipe = models.Recipe.objects.get(id=self.kwargs.get('recipe_id'))
        try:
            models.FavoriteRecipes.objects.create(user=request.user, recipe=recipe)
        except IntegrityError:
            return Response({"errors": "Вы уже добавили товар в избранное!"}, 400)
        serializer = self.serializer_class(recipe)
        return Response(serializer.data, 201)
    
    @action(methods=["delete"], detail=False)
    def delete(self, request, recipe_id):
        try:
            models.Recipe.objects.get(id=recipe_id)
            models.FavoriteRecipes.objects.get(recipe_id=recipe_id, user=request.user).delete()
            return Response(status=204)
        except models.Recipe.DoesNotExist:
            return Response({"errors": "Выбранного рецепта не существует!"}, 400)
        except models.FavoriteRecipes.DoesNotExist:
            return Response({"detail": "Страница не найдена."}, 404)