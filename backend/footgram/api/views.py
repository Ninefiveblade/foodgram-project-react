"""Views module for api app."""
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework.permissions import AllowAny

from .mixins import (
    CustomListRetriveViewSet, RecipeMixin
)
from . import serializers
from cooking import models
from users.models import Follow
from .pagination import ApiPagination
from .viewset_exceptions import (
    check_create, check_delete, check_follow_create, check_follow_delete
)

class RecipeViewSet(RecipeMixin):
    """Recipes viewsets."""
    pagination_class = ApiPagination
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeOutSerializer

    @action(methods=["post", "delete"], detail=True)
    def shopping_cart(self, requset, pk):
        if requset.method == "POST":
            return check_create(
                pk=pk,
                user=requset.user,
                model=models.ShopList
            )
        if requset.method == "DELETE":
            return check_delete(
                pk=pk,
                user=requset.user,
                model=models.ShopList
            )

    @action(methods=["post", "delete"], detail=True)
    def favorite(self, request, pk):
        if request.method == "POST":
            return check_create(
                pk=pk,
                user=request.user,
                model=models.FavoriteRecipes
            )
        elif request.method == "DELETE":
            return check_delete(
                pk=pk,
                user=request.user,
                model=models.FavoriteRecipes
            )

    @action(methods=["get"], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = models.IngredientQuantity.objects.filter(
            recipe_ingredients__in=(user.shop_list_user.values('recipe_id'))
        ).values(
            "ingredients__name",
            "ingredients__measurement"
        ).annotate(amount=Sum('quantity'))
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = ["Список покупок:"]
        for ingredient in ingredients:
            shopping_list.append((
                f'{ingredient.get("ingredients__name")} '
                f'({ingredient.get("ingredients__measurement")}) — '
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


class TagViewSet(CustomListRetriveViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewset(CustomListRetriveViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class FoodgramUserViewSet(UserViewSet):
    """Вьюсет пользователей."""
    pagination_class = ApiPagination
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = serializers.FoodramRegisterInSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            output_serializer = serializers.FoodgramRegisterOutSerializer(user)
            return Response(output_serializer.data)
        else:
            return Response(serializer.errors, 400)
    
    @action(methods=["post", "delete"], detail=True)
    def subscribe(self, request, id):
        if request.method == "POST":
            return check_follow_create(pk=id, user=request.user, model=Follow)
        if request.method == "DELETE":
            return check_follow_delete(pk=id, user=request.user, model=Follow)


    @action(methods=["get"], detail=True)
    def subscriptions(self, request):
        follows = Follow.objects.filter(user=request.user)
        list_of_authors = []
        for follow in follows:
            list_of_authors.append(
                serializers.FoodgramFollowSerializer(follow).data
            )
        return Response(list_of_authors, 200)
