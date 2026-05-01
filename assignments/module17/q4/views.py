from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib import messages
from q3.models import Doctor
from .serializers import DoctorSerializer


@api_view(['GET', 'POST'])
def add_doctor(request):
    """
    GET  — list all doctors
    POST — add a new doctor to the database
    """
    if request.method == 'GET':
        doctors = Doctor.objects.all().order_by('-created_at')
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def doctor_form(request):
    """HTML form to POST a new doctor."""
    doctors = Doctor.objects.all().order_by('-created_at')
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'specialty': request.POST.get('specialty'),
            'contact_email': request.POST.get('contact_email'),
            'contact_phone': request.POST.get('contact_phone'),
            'hospital': request.POST.get('hospital', ''),
            'city': request.POST.get('city', ''),
            'available': request.POST.get('available') == 'on',
        }
        serializer = DoctorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, f"Dr. {data['name']} added successfully!")
            return redirect('q4_form')
        else:
            messages.error(request, f"Validation error: {serializer.errors}")
    return render(request, 'q4/doctor_form.html', {'doctors': doctors})
