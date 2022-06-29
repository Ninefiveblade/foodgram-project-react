from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Recipe(models.Model):
    pass


class Tags(models.Model):
    pass


class Ingredient(models.Model):
    pass