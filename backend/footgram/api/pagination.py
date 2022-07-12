"""Pagination module for api app."""
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class ApiPagination(PageNumberPagination):
    """Кастомный класс пагинации.
    page_size - страницы по умолчанию.
    """
    page_size_query_param = 'limit'


class LolPagination(LimitOffsetPagination):
    offset_query_param = 'recipes_limit'
