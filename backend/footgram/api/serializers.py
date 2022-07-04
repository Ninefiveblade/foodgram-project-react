from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from cooking import models
from users.models import FoodgramUser, Follow


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
    class Meta:
        model = models.Tag
        fields = (
            'id', 'name', 'code', 'slug' 
        )


class FoodgramUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
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

    def to_representation(self, obj):
        ret = super(FoodgramUserSerializer, self).to_representation(obj)
        if self.context.get('request').method == "POST":
            ret.pop('is_subscribed')
        return ret 

    def get_is_subscribed(self, obj):
        return False