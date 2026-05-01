from rest_framework import viewsets, filters
from django.shortcuts import render
from .models import Doctor
from .serializers import DoctorSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    """Full CRUD ViewSet for doctor_finder app."""
    queryset = Doctor.objects.all().order_by('-created_at')
    serializer_class = DoctorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'specialty', 'city']

def doctor_finder_ui(request):
    specialty = request.GET.get('specialty', '')
    city = request.GET.get('city', '')
    doctors = Doctor.objects.all()
    if specialty:
        doctors = doctors.filter(specialty__icontains=specialty)
    if city:
        doctors = doctors.filter(city__icontains=city)
    specialties = Doctor.objects.values_list('specialty', flat=True).distinct()
    cities = Doctor.objects.values_list('city', flat=True).distinct()
    return render(request, 'q9/finder.html', {
        'doctors': doctors,
        'specialties': specialties,
        'cities': cities,
        'selected_specialty': specialty,
        'selected_city': city,
    })
