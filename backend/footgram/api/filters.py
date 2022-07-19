"""Filters module for api app."""
import django_filters as filters

from cooking.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    """Custom filterset for Recipe
    search by tags, name, author."""

    tags = filters.AllValuesMultipleFilter(field_name="tags__slug")
    author = filters.CharFilter(field_name="author_id")

    class Meta:
        model = Recipe
        fields = (
            "author",
        )


class IngredientFilter(filters.FilterSet):
    """Custom filterset for Ingredient
    search by name."""

    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Ingredient
        fields = (
            "name",
        )
