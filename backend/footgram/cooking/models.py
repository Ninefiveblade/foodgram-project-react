"""Cooking app models."""
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import FoodgramUser


class Recipe(models.Model):
    """Recipe model"""

    author: FoodgramUser = models.ForeignKey(
        FoodgramUser,
        verbose_name="Автор рецепта",
        related_name="recipe_user",
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
    image: str = models.ImageField(
        verbose_name="Картинка блюда",
    )
    text: str = models.TextField(
        verbose_name="Описание рецепта",
        help_text="Введите описание рецепта",

    )
    pub_date = models.DateTimeField(auto_now_add=True)
    ingredients = models.ManyToManyField(
        "IngredientQuantity",
        verbose_name="Ингридиенты рецепта",
        help_text="Выберите ингридиенты рецепта",
        related_name="recipe_ingredients",
        blank=False
    )
    time: int = models.IntegerField(
        verbose_name="Время приготовления в минутах",
        help_text="Введите время приготовления в минутах",
        validators=[
            MinValueValidator(1)
        ]
    )
    tags = models.ManyToManyField(
        "Tag",
        verbose_name="Теги по рецептам",
        related_name="recipe_tags",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Tag(models.Model):
    """Tag model."""

    COLOR_PALETTE = [
        ("#E26C2D", "Оранжевый", ),
        ("#228b22", "Зеленый", ),
        ("#9370d8", "Лиловый", ),
    ]
    name: str = models.CharField(
        verbose_name="Имя тега",
        help_text="Введите имя тега",
        max_length=128,
        unique=True,
        db_index=True,
        blank=False
    )
    color: str = ColorField(
        verbose_name="Код цвета HEX",
        max_length=7,
        samples=COLOR_PALETTE,
        unique=True,
        blank=False
    )
    slug: str = models.SlugField(
        verbose_name="slug поле Тега",
        help_text="Введите slug поле Тега",
        max_length=128,
        unique=True,
        db_index=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Тег"
        verbose_name_plural = "Тэги"


class Ingredient(models.Model):
    """Ingredient model."""

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
        ordering = ["id"]
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"


class FavoriteRecipes(models.Model):
    """Favorite recipes model."""

    user: FoodgramUser = models.ForeignKey(
        FoodgramUser,
        verbose_name="Пользователь избранных рецептов",
        related_name="favorite_list_user",
        on_delete=models.CASCADE
    )
    recipe: Recipe = models.ForeignKey(
        "Recipe",
        verbose_name="Избранный рецепт",
        related_name="favorite_recipe",
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_id", "recipe_id"],
                                    name="unique_favorites")
        ]
        ordering = ["id"]
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"


class ShopList(models.Model):
    """Shop basket model."""

    user: FoodgramUser = models.ForeignKey(
        FoodgramUser,
        verbose_name="Пользователь избранных рецептов",
        related_name="shop_list_user",
        on_delete=models.CASCADE
    )
    recipe: Recipe = models.ForeignKey(
        "Recipe",
        verbose_name="Избранный рецепт",
        related_name="shop_recipe",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return (f"Покупки пользователя {self.user.username}, "
                f"c рецептом {self.recipe.name}")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'recipe_id'],
                                    name='unique_shoplist')
        ]
        ordering = ['id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class IngredientQuantity(models.Model):
    """Amount Ingredient model."""

    ingredients: Ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингридиент",
        related_name="ingredients_amount",
        on_delete=models.CASCADE,
        blank=False,
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
        return (
            f"{self.ingredients} "
            f"{self.quantity} "
            f"{self.ingredients.measurement}"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["ingredients", "quantity"],
                                    name="unique_ingredients_quantity")
        ]
        ordering = ['id']
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
