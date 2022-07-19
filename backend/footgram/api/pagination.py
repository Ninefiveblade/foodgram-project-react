"""Pagination module for api app."""
from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class ApiPagination(PageNumberPagination):
    """Custom pagination for all project
    """
    page_size = settings.PAGE_COUNTER
    page_size_query_param = "limit"
