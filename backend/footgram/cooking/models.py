from random import choices
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор рецепта",
        on_delete=models.CASCADE,
        blank=False
    )
    name = models.CharField(
        verbose_name="Название рецепта",
        help_text="Введите название рецепта",
        max_length=128,
        index=True,
        blank=False
    )
    image = models.ImageField(
        verbose_name="Картинка блюда",
    )
    description = models.TextField(
        verbose_name="Описание рецепта",
        help_text="Введите описание рецепта",
        blank=False
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
    tags = models.ManyToOneRel("Tag")

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
        index=True,
        blank=False
    )
    code: str = models.CharField(
        verbose_name="Код цвета HEX",
        help_text="Введите код цвета HEX",
        max_length=128,
        unique=True,
        blank=False
    )
    slug: str = models.SlugField(
        verbose_name="slug поле Тега",
        help_text="Введите slug поле Тега",
        max_length=128,
        unique=True,
        index=True,
        blank=False
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Тэги'

class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Название ингредиента",
        help_text="Введите название ингридиента",
        max_length=128,
        index=True,
        blank=False
    )
    quantity = models.IntegerField(
        verbose_name="Количество ингридиента",
        help_text="Введите количество ингридиента",
        blank=False
    )
    measurement = models.CharField(
        verbose_name="Единица измерения ингридиента",
        help_text="Введите единицу измерения",
        max_length=15
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'