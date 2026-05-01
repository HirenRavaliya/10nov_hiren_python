from rest_framework import generics
from django.shortcuts import render
from django.core.paginator import Paginator
from q3.models import Doctor
from .serializers import DoctorSerializer
from .pagination import DoctorPagination

class DoctorPaginatedList(generics.ListCreateAPIView):
    """Paginated doctor list — 3 per page. Use ?page=2 to navigate."""
    queryset = Doctor.objects.all().order_by('id')
    serializer_class = DoctorSerializer
    pagination_class = DoctorPagination

def pagination_ui(request):
    all_doctors = Doctor.objects.all().order_by('id')
    page_size = int(request.GET.get('page_size', 3))
    paginator = Paginator(all_doctors, page_size)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'q7/pagination.html', {
        'page_obj': page_obj,
        'page_size': page_size,
        'total': all_doctors.count(),
    })
