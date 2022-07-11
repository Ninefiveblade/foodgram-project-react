"""Pagination module for api app."""
from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class ApiPagination(PageNumberPagination):
    """Кастомный класс пагинации.
    page_size - страницы по умолчанию.
    """
    page_size = settings.PAGE_SIZE
