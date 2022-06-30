from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Recipe, Ingredient, Tag

User = get_user_model()


class RecipeAdmin(admin.ModelAdmin):
    """Настройка администрирования для Recipe"""
    list_display = (
        "id",
        "name",
        "description",
        "image",
        "time",
        "author",
        "ingredient",
        "tags",
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "slug"
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "quantity",
        "measurement"
    )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "password",
        "is_active",
        "last_login"
    )

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(User, UserAdmin)

