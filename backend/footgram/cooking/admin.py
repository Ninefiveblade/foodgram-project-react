from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Follow, FoodgramUser

from .models import (FavoriteRecipes, Ingredient, IngredientQuantity, Recipe,
                     ShopList, Tag)


class RecipeAdmin(admin.ModelAdmin):
    """Settings for Recipe model Admin."""

    def favorites_count(self, obj):
        return obj.favorite_recipe.all().count()

    list_display = (
        "name",
        "author",
        "favorites_count"
    )
    list_filter = ("name", "author", "tags")


class TagAdmin(admin.ModelAdmin):
    """Settings for Tag model Admin."""

    list_display = (
        "id",
        "name",
        "color",
        "slug"
    )


class IngredientAdmin(admin.ModelAdmin):
    """Settings for Ingredient model Admin."""

    list_display = (
        "name",
        "measurement"
    )
    list_filter = ("name",)


class FoodgramUserAdmin(UserAdmin):
    """Settings for Foodgram User model Admin."""

    fieldsets = UserAdmin.fieldsets
    list_filter = ("first_name", "email")
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "date_joined",
                    "user_permissions",
                    "first_name",
                    "last_name",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "role",)}
        ),
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(FoodgramUser, FoodgramUserAdmin)
admin.site.register(FavoriteRecipes)
admin.site.register(ShopList)
admin.site.register(Follow)
admin.site.register(IngredientQuantity)
