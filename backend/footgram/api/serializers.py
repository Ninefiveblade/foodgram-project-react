"""Serializers module for api app."""
from rest_framework import serializers

from cooking import models
from .fields import Base64ImageField
from users.models import FoodgramUser, Follow


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient model serializer."""
    measurment_unit = serializers.ReadOnlyField(source="measurement")

    class Meta:
        model = models.Ingredient
        fields = (
            'id',
            'name',
            'measurment_unit'
        )


class IngredientAmountInSerializer(serializers.ModelSerializer):
    """IngredientQuantity models serializer."""
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=models.Ingredient.objects.all()
    )
    amount = serializers.IntegerField(source='quantity')

    class Meta:
        model = models.IngredientQuantity
        fields = (
            'id',
            'amount',
        )


class IngredientAmountOutSerializer(serializers.ModelSerializer):
    """IngredientQuantity model serializer for GET requests."""
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    amount = serializers.ReadOnlyField(source="quantity")
    measurment_unit = serializers.ReadOnlyField(
        source="ingredient.measurement"
    )

    class Meta:
        model = models.IngredientQuantity
        fields = (
            'id',
            'name',
            'measurment_unit',
            'amount',
        )


class TagSerializer(serializers.ModelSerializer):
    """Tag model serializer."""
    class Meta:
        model = models.Tag
        fields = (
            'id', 'name', 'code', 'slug'
        )


class FoodgramUserSerializer(serializers.ModelSerializer):
    """FoodgramUser model serializer."""
    is_subscribed = serializers.SerializerMethodField()
    # доделать
    class Meta:
        model = FoodgramUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return None


class RecipeSerializer(serializers.ModelSerializer):
    """Resipe model POST/PATCH/DELETE requests serializer."""
    author = FoodgramUserSerializer(read_only=True)
    ingredient = IngredientAmountInSerializer(many=True)
    current_time = serializers.IntegerField(source="time")
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = models.Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredient',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'text',
            'current_time',
        )

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredient")
        recipe = models.Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients:
            ingredient, bool = (
                models.IngredientQuantity.objects.get_or_create(
                    **ingredient_data
                )
            )
            recipe.ingredient.add(ingredient)
        for tag_data in tags:
            tag = models.Tag.objects.get(id=tag_data.id)
            recipe.tags.add(tag)
        return recipe
    
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')
        ingredient_list = []
        for ingredient_data in ingredients:
            ingredient, bool = (
                models.IngredientQuantity.objects.get_or_create(
                    **ingredient_data
                )
            )
            ingredient_list.append(ingredient)
        instance.ingredient.set(ingredient_list)
        instance.tags.set(tags)
        instance.text = validated_data.get('text', instance.text)
        instance.name = validated_data.get('name', instance.name)
        instance.time = validated_data.get('time', instance.time)
        return instance
        

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class RecipeOutSerializer(RecipeSerializer):
    """Resipe model POST response/GET requests serializer."""
    ingredient = IngredientAmountOutSerializer(many=True)
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
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = RecipeShortSerializer(many=True, read_only=True)

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
        )

    def create(self, validated_data):
        return Follow.objects.create(**validated_data)
