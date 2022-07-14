"""Serializers module for api app."""
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import Follow, FoodgramUser
from cooking import models


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
        source='ingredients',
        queryset=models.Ingredient.objects.all()
    )
    amount = serializers.IntegerField(source="quantity")

    class Meta:
        model = models.IngredientQuantity
        fields = (
            "id",
            "amount",
        )


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

    is_subscribed = serializers.SerializerMethodField()

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
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return obj.following.filter(user=user).exists()


class FoodramRegisterInSerializer(serializers.ModelSerializer):
    """Foodram Rerister input serializer."""

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


class FoodgramRegisterOutSerializer(serializers.ModelSerializer):
    """Foodram Rerister out serializer."""

    class Meta:
        model = FoodgramUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
        )


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
        for tag_data in tags:
            tag = models.Tag.objects.get(id=tag_data.id)
            recipe.tags.add(tag)
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
        instance.text = validated_data.get("text", instance.text)
        instance.name = validated_data.get("name", instance.name)
        instance.time = validated_data.get("time", instance.time)
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return obj.favorite_recipe.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return obj.shop_recipe.filter(user=user).exists()


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

    def create(self, validated_data):
        return Follow.objects.create(**validated_data)

    def get_recipes_count(self, obj):
        return obj.author.recipe_user.all().count()

    def get_recipes(self, obj):
        recipe_limit = self.context.get(
            "request"
        ).query_params.get("recipes_limit")
        if recipe_limit is not None:
            recipes = obj.author.recipe_user.all()[:int(recipe_limit)]
            return RecipeShortSerializer(instance=recipes, many=True).data
        return RecipeShortSerializer(instance=obj, many=True).data

    def get_is_subscribed(self, obj):
        return True
