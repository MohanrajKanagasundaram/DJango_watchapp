from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class ReviewPagination(PageNumberPagination):
    page_size=3
    page_query_param='record'
    page_size_query_param='size'
    max_page_size=3
    last_page_strings='end'

class MovieListPagination(LimitOffsetPagination):
    default_limit=1
    max_limit=5
    
    