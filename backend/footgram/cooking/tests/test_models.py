from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Ingredient, Recipe, Tag

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="test_user")
        cls.ingredient = Ingredient.objects.create(
            name="test_name",
            quantity=1,
            measurement="кг"
        )
        cls.tag = Tag.objects.create(
            name="test_tag",
            code="test_code",
            slug="test_slug"
        )
        cls.recipe = Recipe(
            ...
        )
