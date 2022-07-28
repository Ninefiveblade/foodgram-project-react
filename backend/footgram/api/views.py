"""Views module for api app."""
from http import HTTPStatus

from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import Follow
from cooking import models
from . import serializers
from .filters import IngredientFilter, RecipeFilter
from .mixins import CustomListRetriveViewSet, RecipeMixin
from .pagination import ApiPagination
from .permissions import RecipeIsStaffOrOwner
from .utils import (check_create, check_delete, check_follow_create,
                    check_follow_delete, download)


class RecipeViewSet(RecipeMixin):
    """Recipes viewsets."""

    pagination_class = ApiPagination
    serializer_class = serializers.RecipeOutSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (RecipeIsStaffOrOwner,)

    def get_queryset(self):
        user = self.request.user
        queryset = models.Recipe.objects.all()
        is_favorited = self.request.query_params.get("is_favorited")
        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart"
        )
        if is_favorited is not None:
            queryset = queryset.filter(favorite_recipe__user=user)
        if is_in_shopping_cart is not None:
            queryset = queryset.filter(shop_recipe__user=user)
        return queryset.order_by("-pub_date")

    @action(
        methods=["post", "delete"], detail=True
    )
    def shopping_cart(self, requset, pk):
        if requset.method == "POST":
            return check_create(
                pk=pk,
                user=requset.user,
                model=models.ShopList
            )
        return check_delete(
            pk=pk,
            user=requset.user,
            model=models.ShopList
        )

    @action(
        methods=["post", "delete"], detail=True
    )
    def favorite(self, request, pk):
        if request.method == "POST":
            return check_create(
                pk=pk,
                user=request.user,
                model=models.FavoriteRecipes
            )
        return check_delete(
            pk=pk,
            user=request.user,
            model=models.FavoriteRecipes
        )

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        return download(self, request)

    def create(self, request, *args, **kwargs):
        serializer = serializers.RecipeSerializer(
            data=request.data,
            context={"request": self.request}
        )
        if serializer.is_valid(raise_exception=True):
            recipe = serializer.save(author=self.request.user)
            output_serializer = serializers.RecipeOutSerializer(
                recipe, context={"request": request}
            )
            return Response(output_serializer.data)
        else:
            return Response(serializer.errors, HTTPStatus.BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.RecipeSerializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            recipe = serializer.save()
            output_serializer = serializers.RecipeOutSerializer(
                recipe, context={"request": request}
            )
            return Response(output_serializer.data)
        else:
            return Response(serializer.errors, HTTPStatus.BAD_REQUEST)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve",):
            return serializers.RecipeOutSerializer
        if self.action in ("partial_update",):
            return serializers.RecipeOutSerializer


class TagViewSet(CustomListRetriveViewSet):
    """Tag viewset."""

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class IngredientViewset(CustomListRetriveViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FoodgramUserViewSet(UserViewSet):
    """User viewset."""

    pagination_class = ApiPagination

    def create(self, request, *args, **kwargs):
        serializer = serializers.FoodramRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, HTTPStatus.BAD_REQUEST)

    @action(methods=["post", "delete"], detail=True)
    def subscribe(self, request, id):
        if request.method == "POST":
            return check_follow_create(
                pk=id, user=request.user, model=Follow, request=request
            )
        return check_follow_delete(pk=id, user=request.user, model=Follow)

    @action(
        methods=["get"], detail=False, permission_classes=[IsAuthenticated, ]
    )
    def subscriptions(self, request):
        paginator = self.pagination_class()
        follow_objects = Follow.objects.filter(user=request.user)
        result_page = paginator.paginate_queryset(follow_objects, request)
        serializer = serializers.FoodgramFollowSerializer(
            result_page, many=True, context={"request": self.request}
        )
        return paginator.get_paginated_response(serializer.data)
