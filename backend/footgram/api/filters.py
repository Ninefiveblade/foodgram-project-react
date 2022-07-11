"""Filters module for api app."""
import django_filters as filters
from cooking.models import Recipe


class RecipeFilter(filters.FilterSet):
    """Кастомный фильтр для вьюсета Recipe
    поиск по полям genre, category."""
    tags = filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='icontains'
    )
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Recipe
        fields = ('name', 'genre', 'category', 'year')


class IngredientFilter(filters.FilterSet):
    pass
