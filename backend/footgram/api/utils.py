"""Utils help module for ViewSets."""
from http import HTTPStatus

from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from cooking import models
from . import serializers


def check_create(pk, model, user):
    """Shop/Favorite recipe create optimization."""
    recipe = get_object_or_404(models.Recipe, id=pk)
    try:
        model.objects.create(user=user, recipe=recipe)
    except IntegrityError:
        return Response(
            {"errors": "Вы уже добавили товар !"}, HTTPStatus.BAD_REQUEST
        )
    serializer = serializers.RecipeShortSerializer(recipe)
    return Response(serializer.data, HTTPStatus.CREATED)


def check_delete(pk, model, user):
    """Shop/Favorite recipe delete optimization."""
    recipe = get_object_or_404(models.Recipe, id=pk)
    get_object_or_404(model, recipe_id=recipe.id, user=user).delete()
    return Response(status=HTTPStatus.NO_CONTENT)


def check_follow_create(pk, model, user):
    """Create follow optimization."""
    try:
        author = get_object_or_404(models.FoodgramUser, id=pk)
        if author == user:
            return Response(
                {"errors": "Вы не можете подписаться сами на себя!"},
                HTTPStatus.BAD_REQUEST
            )
        model.objects.create(user=user, author=author)
        return Response(status=HTTPStatus.NO_CONTENT)
    except IntegrityError:
        return Response(
            {"errors": "Вы уже подписаны на этого автора!"},
            HTTPStatus.BAD_REQUEST
        )


def check_follow_delete(pk, model, user):
    """Delete follow optimization."""
    try:
        get_object_or_404(models.FoodgramUser, id=pk)
        model.objects.get(author_id=pk, user_id=user.id).delete()
        return Response(status=HTTPStatus.NO_CONTENT)
    except model.DoesNotExist:
        return Response(
            {"errors": "Вы не подписаны на данного автора."},
            HTTPStatus.BAD_REQUEST
        )


def get_additional_field(self, obj_related):
    """Get additional SerializerField optimzation."""
    try:
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return obj_related.filter(user=user).exists()
    except Exception:
        return False


def download(self, request):
    """Download shopping card."""
    user = request.user
    ingredients = models.IngredientQuantity.objects.filter(
        recipe_ingredients__in=(user.shop_list_user.values("recipe_id"))
    ).values(
        "ingredients__name",
        "ingredients__measurement"
    ).annotate(amount=Sum('quantity')).order_by("-total")
    filename = f"{user.username}_shopping_list.txt"
    shopping_list = ["Список покупок:"]
    for ingredient in ingredients:
        shopping_list.append((
            f'{ingredient.get("ingredients__name")} '
            f'({ingredient.get("ingredients__measurement")}) — '
            f'{ingredient.get("amount")}'
        ).capitalize())
    response = HttpResponse(
        "\n".join(shopping_list), content_type="text.txt; charset=utf-8"
    )
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
