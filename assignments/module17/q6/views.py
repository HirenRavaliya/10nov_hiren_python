from rest_framework import viewsets
from django.shortcuts import render
from q3.models import Doctor
from .serializers import DoctorSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    """
    DRF ModelViewSet registered with DefaultRouter.
    Automatically routes:
      GET    /q6/doctors/        — list
      POST   /q6/doctors/        — create
      GET    /q6/doctors/<id>/   — retrieve
      PUT    /q6/doctors/<id>/   — update
      PATCH  /q6/doctors/<id>/   — partial_update
      DELETE /q6/doctors/<id>/   — destroy
    """
    queryset = Doctor.objects.all().order_by('-created_at')
    serializer_class = DoctorSerializer

def router_ui(request):
    doctors = Doctor.objects.all().order_by('-created_at')
    return render(request, 'q6/routing.html', {'doctors': doctors})
