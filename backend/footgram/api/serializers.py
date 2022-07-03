from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from cooking import models
from users.models import FoodgramUser

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = (
            'id', 'name', 'measurement'
        )

class RecipeSerializer(serializers.ModelSerializer):
    ingregient = IngredientSerializer(many=True)
    class Meta:
        model = models.Ingredient
        fields = (
            'id', 'name', 'ingregient', 
        )


class TagSerializer(serializers.ModelSerializer):
    pass



class UserSerializer(serializers.ModelSerializer):
    pass

class CustomUserCreateSerializer(UserCreateSerializer):
    User = FoodgramUser()
    
    pass

