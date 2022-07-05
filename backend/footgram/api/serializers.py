from jinja2 import pass_context
from rest_framework import serializers

from cooking import models
from users.models import FoodgramUser, Follow


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.RelatedField(source='ingredient_id__', read_only=True)
    amount = serializers.IntegerField(source='quantity')
    class Meta:
        model = models.IngredientQuantity
        fields = (
            'id',
            'amount',
        )

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = (
            'id',
            'name',
            'measurement',
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


class RecipeSerializer(serializers.ModelSerializer):
    author = FoodgramUserSerializer(read_only=True)
    ingredient = IngredientAmountSerializer(many=True)
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
            'time',
        )
    
    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def get_is_favorited(self, obj):
        return False
    
    def get_is_in_shopping_cart(self, obj):
        return False
