"""Pagination module for api app."""
from rest_framework.pagination import PageNumberPagination


class ApiPagination(PageNumberPagination):
    """Кастомный класс пагинации.
    page_size - страницы по умолчанию.
    """
    page_size_query_param = 'limit'
