"""Users app models."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class FoodgramUser(AbstractUser):
    """Custom yser model."""

    USER = "user"
    ADMIN = "admin"
    ROLES = [
        (USER, "User"),
        (ADMIN, "Administrator"),
    ]

    first_name: str = models.CharField(max_length=150, blank=False)
    last_name: str = models.CharField(max_length=150, blank=False)
    email: str = models.EmailField(max_length=254, blank=False, unique=True)
    password: str = models.CharField(max_length=150, blank=False)
    role: str = models.CharField(max_length=100, choices=ROLES, default=USER)

    @property
    def is_admin(self):
        return self.is_superuser or self.role == FoodgramUser.ADMIN

    @property
    def is_user(self):
        return self.role == FoodgramUser.USER

    class Meta:
        ordering = ["-username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Follow(models.Model):
    """Follows model."""

    user: FoodgramUser = models.ForeignKey(
        FoodgramUser,
        help_text="Подписчик",
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author: FoodgramUser = models.ForeignKey(
        FoodgramUser,
        help_text="Автор",
        on_delete=models.CASCADE,
        related_name='following'
    )

    def __str__(self) -> str:
        return f"На {self.author.username}, подписан {self.user.username}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_id", "author_id"],
                                    name="unique_follows")
        ]
        ordering = ["id"]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
