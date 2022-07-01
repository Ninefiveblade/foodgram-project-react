from django.db import models
from django.contrib.auth import get_user_model

from users.models import FoodgramUser
from colorfield.fields import ColorField

User = get_user_model()


class Recipe(models.Model):
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
    time = models.TimeField(
        help_text="Время приготовления"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Tag(models.Model):
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
        help_text="Введите код цвета HEX",
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
    name: str = models.CharField(
        verbose_name="Название ингредиента",
        help_text="Введите название ингридиента",
        max_length=128,
        db_index=True,
        blank=False
    )
    quantity: int = models.IntegerField(
        verbose_name="Количество ингридиента",
        help_text="Введите количество ингридиента",
        null=True,
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
