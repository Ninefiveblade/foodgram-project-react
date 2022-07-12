from rest_framework.response import Response
from django.db import IntegrityError

from cooking import models
from . import serializers


def check_create(pk, model, user):
    try:
        recipe = models.Recipe.objects.get(id=pk)
    except models.Recipe.DoesNotExist:
        return Response(
            {"errors": "Выбранного рецепта не существует!"}, 400
        )
    try:
        model.objects.create(user=user, recipe=recipe)
    except IntegrityError:
        return Response(
            {"errors": "Вы уже добавили товар !"}, 400
        )
    serializer = serializers.RecipeShortSerializer(recipe)
    return Response(serializer.data, 201)


def check_delete(pk, model, user):
    try:
        recipe = models.Recipe.objects.get(id=pk)
    except models.Recipe.DoesNotExist:
        return Response(
            {"errors": "Выбранного рецепта не существует!"}, 400
        )
    try:
        model.objects.get(recipe_id=recipe.id, user=user).delete()
        return Response(status=204)
    except model.DoesNotExist:
        return Response({"detail": "Страница не найдена."}, 404)


def check_follow_create(pk, model, user):
    try:
        author = models.FoodgramUser.objects.get(id=pk)
        if author == user:
            return Response(
                {"errors": "Вы не можете подписаться сами на себя!"},
                400
            )
        model.objects.create(user=user, author=author)
        return Response(status=204)
    except IntegrityError:
        return Response(
            {"errors": "Вы уже подписаны на этого автора!"}, 400
        )
    except models.FoodgramUser.DoesNotExist:
        return Response({"detail": "Страница не найдена."}, status=404)


def check_follow_delete(pk, model, user):
    try:
        models.FoodgramUser.objects.get(id=pk)
        model.objects.get(author_id=pk, user_id=user.id).delete()
        return Response(status=204)
    except model.DoesNotExist:
        return Response(
            {"errors": "Вы не подписаны на данного автора."}, status=400
        )
    except models.FoodgramUser.DoesNotExist:
        return Response({"detail": "Страница не найдена."}, status=404)
