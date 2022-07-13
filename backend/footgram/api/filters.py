"""Filters module for api app."""
import django_filters as filters

from cooking.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    """Кастомный фильтр для вьюсета Recipe
    поиск по полям tags, category."""
    tags = filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='icontains'
    )
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author_id')

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags'
        )


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = (
            'name',
        )
