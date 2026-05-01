from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Doctor
from .serializers import DoctorSerializer


@api_view(['GET'])
def doctor_list(request):
    """List all doctors — demonstrates serialization."""
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def doctor_detail(request, pk):
    """Get a single doctor — demonstrates serialization of single object."""
    try:
        doctor = Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=404)
    serializer = DoctorSerializer(doctor)
    return Response(serializer.data)


def doctor_ui(request):
    """HTML frontend to browse serialized doctors."""
    doctors = Doctor.objects.all()
    return render(request, 'q3/doctors.html', {'doctors': doctors})
