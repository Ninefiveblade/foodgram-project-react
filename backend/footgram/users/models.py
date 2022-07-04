"""Модели приложения users."""
from django.db import models
from django.contrib.auth.models import AbstractUser, AnonymousUser


class FoodgramUser(AbstractUser):
    """Кастомная модель юзера."""
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'User'),
        (ADMIN, 'Administrator'),
    ]

    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    password = models.CharField(max_length=150, blank=False)
    role = models.CharField(max_length=100, choices=ROLES, default=USER)

    @property
    def is_admin(self):
        return self.is_superuser or self.role == FoodgramUser.ADMIN
    
    @property
    def is_user(self):
        return self.role == FoodgramUser.USER
    
    class Meta:
        ordering = ['-username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Guest(AnonymousUser):
    """Модель гостя"""
    def __str__(self):
        return 'Guest'

    @property
    def is_guest(self):
        return True


class Follow(models.Model):
    """Модели подписок."""
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follows')
        ]
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'