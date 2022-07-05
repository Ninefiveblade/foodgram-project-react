from django.contrib import admin

from .models import Recipe, Ingredient, Tag, FavoriteRecipes, ShopList, IngredientQuantity
from users.models import FoodgramUser, Follow


class RecipeAdmin(admin.ModelAdmin):
    """Настройка администрирования для Recipe"""
    list_display = (
        "name",
        "author"
    )
    list_filter = ("name", "author", "tags")


class TagAdmin(admin.ModelAdmin):
    """Настройка администрирования для Tag"""
    list_display = (
        "id",
        "name",
        "code",
        "slug"
    )


class IngredientAdmin(admin.ModelAdmin):
    """Настройка администрирования для Ingredient"""
    list_display = (
        "name",
        "measurement"
    )
    list_filter = ("name",)


class FoodgramUserAdmin(admin.ModelAdmin):
    """Настройка администрирования FoodgramUser."""
    list_display = (
        "username",
        "first_name",
        "email"
    )
    list_filter = ("first_name", "email")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(FoodgramUser, FoodgramUserAdmin)
admin.site.register(FavoriteRecipes)
admin.site.register(ShopList)
admin.site.register(Follow)
admin.site.register(IngredientQuantity)