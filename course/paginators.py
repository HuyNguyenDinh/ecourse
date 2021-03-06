from rest_framework.pagination import PageNumberPagination

class CategoryPagination(PageNumberPagination):
    page_size = 8

class BasePagination(PageNumberPagination):
    page_size = 20