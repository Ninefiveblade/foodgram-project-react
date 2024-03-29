"""Serializers module for api app."""
from drf_extra_fields.fields import Base64ImageField
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import ValidationError

from users.models import Follow, FoodgramUser
from cooking import models
from .utils import get_additional_field, validate


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient model serializer."""

    measurement_unit = serializers.ReadOnlyField(source="measurement")

    class Meta:
        model = models.Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit"
        )


class IngredientAmountInSerializer(serializers.ModelSerializer):
    """IngredientQuantity models serializer."""

    id = serializers.PrimaryKeyRelatedField(
        source="ingredients",
        queryset=models.Ingredient.objects.all()
    )
    amount = serializers.IntegerField(source="quantity")

    class Meta:
        model = models.IngredientQuantity
        fields = (
            "id",
            "amount",
        )

    def validate_amount(self, amount):
        if amount < 1:
            raise ValidationError('Количество не может быть меньше 1')
        return amount


class IngredientAmountOutSerializer(serializers.ModelSerializer):
    """IngredientQuantity model serializer for GET requests."""

    id = serializers.ReadOnlyField(source="ingredients.id")
    name = serializers.ReadOnlyField(source="ingredients.name")
    amount = serializers.ReadOnlyField(source="quantity")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredients.measurement"
    )

    class Meta:
        model = models.IngredientQuantity
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class TagSerializer(serializers.ModelSerializer):
    """Tag model serializer."""

    class Meta:
        model = models.Tag
        fields = (
            "id", "name", "color", "slug"
        )


class FoodgramUserSerializer(serializers.ModelSerializer):
    """FoodgramUser model serializer."""

    is_subscribed = serializers.SerializerMethodField(
        method_name="get_is_subscribed"
    )

    class Meta:
        model = FoodgramUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed"
        )

    def get_is_subscribed(self, obj):
        return get_additional_field(self, obj.following)


class FoodramRegisterSerializer(serializers.ModelSerializer):
    """Foodram Rerister serializer."""

    class Meta:
        model = FoodgramUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password"
        )
        extra_kwargs = {
            "password": {'write_only': True}
        }

    def validate_username(self, username):
        if not username.isalpha():
            raise ValidationError('Имя должно иметь только буквы!')
        if len(username) < settings.MIN_LEN_USERNAME:
            raise ValidationError(
                'Username не может быть меньше 5 символов!'
            )
        return username.lower()


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe model POST/PATCH/DELETE requests serializer."""

    author = FoodgramUserSerializer(read_only=True)
    ingredients = IngredientAmountInSerializer(many=True)
    cooking_time = serializers.IntegerField(source="time")
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(
        method_name="get_is_favorited"
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name="get_is_in_shopping_cart"
    )

    class Meta:
        model = models.Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = models.Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients:
            ingredient, bool = (
                models.IngredientQuantity.objects.get_or_create(
                    **ingredient_data
                )
            )
            recipe.ingredients.add(ingredient)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        ingredient_list = []
        for ingredient_data in ingredients:
            ingredient, bool = (
                models.IngredientQuantity.objects.get_or_create(
                    **ingredient_data
                )
            )
            ingredient_list.append(ingredient)
        instance.ingredients.set(ingredient_list)
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def validate_name(self, name):
        return validate(
            name,
            settings.MIN_LEN_NAME,
            settings.MAX_LEN_NAME
        )

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise ValidationError("Время не может быть меньше 1 мин.")
        return cooking_time

    def get_is_favorited(self, obj):
        return get_additional_field(self, obj.favorite_recipe)

    def get_is_in_shopping_cart(self, obj):
        return get_additional_field(self, obj.shop_recipe)


class RecipeOutSerializer(RecipeSerializer):
    """Resipe model POST response/GET requests serializer."""

    ingredients = IngredientAmountOutSerializer(many=True)
    tags = TagSerializer(many=True)


class RecipeShortSerializer(serializers.ModelSerializer):
    """Short recipe serializer."""

    cooking_time = serializers.IntegerField(source="time")

    class Meta:
        model = models.Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time"
        )


class FoodgramFollowSerializer(serializers.Serializer):
    """Follow serializer."""

    email = serializers.ReadOnlyField(source="author.email")
    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = serializers.SerializerMethodField(
        method_name="get_is_subscribed"
    )
    recipes = serializers.SerializerMethodField(method_name="get_recipes")
    recipes_count = serializers.SerializerMethodField(
        method_name="get_recipes_count"
    )

    class Meta:
        model = Follow
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count"
        )

    def get_recipes_count(self, obj):
        return obj.author.recipe_user.all().count()

    def get_recipes(self, obj):
        recipes = obj.author.recipe_user.all()
        recipe_limit = self.context.get(
            "request"
        ).query_params.get("recipes_limit")
        if recipe_limit is not None:
            recipes = obj.author.recipe_user.all()[:int(recipe_limit)]
            return RecipeShortSerializer(instance=recipes, many=True).data
        return RecipeShortSerializer(instance=recipes, many=True).data

    def get_is_subscribed(self, obj):
        return True
