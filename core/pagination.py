"""Pagination helpers for the API.

This module defines a reusable page number pagination class that supports
page size customization through query parameters.
"""

from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Page number pagination with a configurable page size."""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
