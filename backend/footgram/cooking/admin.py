from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django import forms

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
        "color",
        "slug"
    )


class IngredientAdmin(admin.ModelAdmin):
    """Настройка администрирования для Ingredient"""
    list_display = (
        "name",
        "measurement"
    )
    list_filter = ("name",)


class FoodgramUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = FoodgramUser
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            FoodgramUser.objects.get(username=username)
        except FoodgramUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

class FoodgramUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    list_filter = ("first_name", "email")
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'date_joined',
                'user_permissions',
                'first_name',
                'last_name',
                'is_superuser',
                'is_staff',
                'is_active',
                'role',
            )}
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