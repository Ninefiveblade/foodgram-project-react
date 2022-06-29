from random import choices
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        help_text="Автор рецепта",
        on_delete=models.CASCADE,
        blank=False
    )
    name = models.CharField(
        help_text="Название рецепта",
        max_length=128,
        index=True,
        blank=False
    )
    image = models.ImageField()
    description = models.TextField(
        help_text="Описание рецепта",
        blank=False
    )
    ingredient = models.ManyToManyField(
        "Ingredient",
        help_text="Ингридиенты рецента",
        related_name="reciepe_ingredient",
        blank=False
    )
    time = models.TimeField(
        help_text="Время приготовления"
    )
    #tags = models.ManyToOneRel("Tags")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'




class Tags(models.Model):
    name: str = models.CharField(
        help_text="Имя тега",
        max_length=128,
        unique=True,
        index=True,
        blank=False
    )
    code: str = models.CharField(
        help_text="Код цвета HEX",
        max_length=128,
        unique=True,
        blank=False
    )
    slug: str = models.SlugField(
        help_text="slug поле Тега",
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
        help_text="Название ингридиента",
        max_length=128,
        index=True,
        blank=False
    )
    quantity = models.IntegerField(
        help_text="Количество ингридиента",
        blank=False
    )
    measurement = models.CharField(
        max_length=15,
        help_text="Единица измерения ингридиента"
    )