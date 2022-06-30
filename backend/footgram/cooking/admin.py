from django.contrib import admin

from .models import Recipe, Ingredient, Tag


class RecipeAdmin(admin.ModelAdmin):
    """Настройка администрирования для Recipe"""
    list_display = (
        "id",
        "name",
        "description",
        "image",
        "time",
        "author",
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "slug",
        "recipe"
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "quantity",
        "measurement"
    )

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
