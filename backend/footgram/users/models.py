from django.db import models
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.contrib.auth import get_user




class FoodgramUser(AbstractUser):
    """Кастомная модель юзера."""
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'User'),
        (ADMIN, 'Administrator'),
    ]

    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)

    role = models.CharField(max_length=100, choices=ROLES, default=USER)

    @property
    def is_admin(self):
        return self.is_superuser or self.role == FoodgramUser.ADMIN
    
    @property
    def is_user(self):
        return self.role == FoodgramUser.USER
    
    class Meta:
        ordering = ['-username']


# Под вопросом
class Guest(AnonymousUser):
    """Модель гостя"""
    def __str__(self):
        return 'Guest'

    @property
    def is_guest(self):
        return True
