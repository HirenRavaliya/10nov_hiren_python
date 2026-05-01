from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from q3.models import Doctor
from .serializers import DoctorSerializer

class DoctorList(generics.ListCreateAPIView):
    """GET /q11/doctors/ — list all | POST — create"""
    queryset = Doctor.objects.all().order_by('-created_at')
    serializer_class = DoctorSerializer

class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /q11/doctors/<id>/"""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

def restful_ui(request):
    doctors = Doctor.objects.all().order_by('-created_at')
    return render(request, 'q11/restful.html', {'doctors': doctors})
