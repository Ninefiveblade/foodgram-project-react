"""Filters module for api app."""
import django_filters as filters

from cooking.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    """Custom filterset for Recipe
    search by tags, name, author."""

    tags = filters.CharFilter(
        field_name="tags__slug",
        method='filter_tags'
    )
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    author = filters.CharFilter(field_name="author_id")

    def filter_tags(self, queryset, slug, tags):
        return queryset.filter(tags__slug__contains=tags.split(','))

    class Meta:
        model = Recipe
        fields = (
            "author",
            "tags"
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
