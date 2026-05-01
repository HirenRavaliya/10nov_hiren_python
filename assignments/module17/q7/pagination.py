from rest_framework.pagination import PageNumberPagination

class DoctorPagination(PageNumberPagination):
    page_size = 3                    # 3 doctors per page
    page_size_query_param = 'page_size'
    max_page_size = 20
