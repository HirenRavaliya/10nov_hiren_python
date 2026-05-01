from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DoctorLocation
from .serializers import DoctorLocationSerializer

@api_view(['GET'])
def doctor_locations_api(request):
    city = request.GET.get('city', '')
    doctors = DoctorLocation.objects.all()
    if city:
        doctors = doctors.filter(city__icontains=city)
    serializer = DoctorLocationSerializer(doctors, many=True)
    return Response(serializer.data)

def doctor_map(request):
    city = request.GET.get('city', '')
    doctors = DoctorLocation.objects.all()
    if city:
        doctors = doctors.filter(city__icontains=city)
    cities = DoctorLocation.objects.values_list('city', flat=True).distinct()

    if request.method == 'POST':
        try:
            DoctorLocation.objects.create(
                name=request.POST.get('name'),
                specialty=request.POST.get('specialty'),
                hospital=request.POST.get('hospital'),
                city=request.POST.get('city'),
                address=request.POST.get('address'),
                latitude=float(request.POST.get('latitude', 0)),
                longitude=float(request.POST.get('longitude', 0)),
                contact_phone=request.POST.get('contact_phone', ''),
                available=request.POST.get('available') == 'on',
            )
            messages.success(request, 'Doctor location added!')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('/q22/')

    return render(request, 'q22/map.html', {
        'doctors': doctors,
        'cities': cities,
        'selected_city': city,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
    })
