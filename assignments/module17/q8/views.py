from rest_framework import generics
from django.shortcuts import render
import os
from django.conf import settings
from q3.models import Doctor
from .serializers import DoctorSerializer

class DoctorList(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

def sqlite_ui(request):
    doctors = Doctor.objects.all()
    db_path = settings.DATABASES['default']['NAME']
    db_size = os.path.getsize(db_path) if os.path.exists(str(db_path)) else 0
    return render(request, 'q8/sqlite.html', {
        'doctors': doctors,
        'db_path': db_path,
        'db_size': round(db_size / 1024, 2),
    })
