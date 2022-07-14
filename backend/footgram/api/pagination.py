"""Pagination module for api app."""
from rest_framework.pagination import PageNumberPagination


class ApiPagination(PageNumberPagination):
    """Custom pagination for all project
    """
    page_size_query_param = 'limit'
