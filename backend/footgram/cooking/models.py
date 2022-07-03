"""Модели приложения cooking."""
from django.db import models
from django.core.validators import MinValueValidator

from colorfield.fields import ColorField

from users.models import FoodgramUser


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        FoodgramUser,
        verbose_name="Автор рецепта",
        on_delete=models.CASCADE,
        db_index=True,
        blank=False
    )
    name: str = models.CharField(
        verbose_name="Название рецепта",
        help_text="Введите название рецепта",
        max_length=128,
        db_index=True,
        blank=False
    )
    image = models.ImageField(
        verbose_name="Картинка блюда",
    )
    description: str = models.TextField(
        verbose_name="Описание рецепта",
        help_text="Введите описание рецепта",

    )
    ingredient = models.ManyToManyField(
        "Ingredient",
        verbose_name="Ингридиенты рецепта",
        help_text="Выберите ингридиенты рецепта",
        related_name="reciepe_ingredient",
        blank=False
    )
    time = models.IntegerField(
        verbose_name="Время приготовления в минутах",
        help_text="Введите время приготовления в минутах",
        validators=[
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Tag(models.Model):
    """Модель тега."""
    name: str = models.CharField(
        verbose_name="Имя тега",
        help_text="Введите имя тега",
        max_length=128,
        unique=True,
        db_index=True,
        blank=False
    )
    code: str = ColorField(
        verbose_name="Код цвета HEX",
        max_length=7,
        unique=True,
        blank=False
    )
    slug: str = models.SlugField(
        verbose_name="slug поле Тега",
        help_text="Введите slug поле Тега",
        max_length=128,
        unique=True,
        db_index=True,
        blank=False
    )
    recipe = models.ManyToManyField(
        "Recipe",
        verbose_name="Теги по рецептам",
        related_name="recipe_tag"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    """Модель ингридиента."""
    name: str = models.CharField(
        verbose_name="Название ингредиента",
        help_text="Введите название ингридиента",
        max_length=128,
        db_index=True,
        blank=False
    )
    measurement: str = models.CharField(
        verbose_name="Единица измерения ингридиента",
        help_text="Введите единицу измерения",
        max_length=15
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class FavoriteRecipes(models.Model):
    """Модель избранного."""
    user = models.ForeignKey(
        FoodgramUser,
        verbose_name="Пользователь избранных рецептов",
        related_name="favotite_list_user",
        on_delete=models.CASCADE
    )
    recipe = models.ManyToManyField(
        "Recipe",
        verbose_name="Избранный рецепт",
        related_name="favorite_recipe"
    )
    class Meta:
        ordering = ['id']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShopList(models.Model):
    """Модель покупок."""
    user = models.ForeignKey(
        FoodgramUser,
        verbose_name="Пользователь избранных рецептов",
        related_name="shop_list_user",
        on_delete=models.CASCADE
    )
    recipe = models.ManyToManyField(
        "Recipe",
        verbose_name="Избранный рецепт",
        related_name="shop_recipe"
    )
    class Meta:
        ordering = ['id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингридиент",
        related_name="ingredient_amount",
        null=True,
        on_delete=models.SET_NULL
    )
    quantity: int = models.IntegerField(
        verbose_name="Количество ингридиента",
        help_text="Введите количество ингридиента",
        validators=[
            MinValueValidator(1)
        ],
        null=True,
        blank=False
    )
    
    def __str__(self):
        return f"id: {self.id}, {self.ingredient} {self.quantity} {self.ingredient.measurement}"
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'