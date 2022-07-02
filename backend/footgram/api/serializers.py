from rest_framework import serializers

from cooking import models
from users.models import FoodgramUser


class RecipeSerializer(serializers.ModelSerializer):
    pass


class TagSerializer(serializers.ModelSerializer):
    pass


class IngredientSerializer(serializers.ModelSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    pass