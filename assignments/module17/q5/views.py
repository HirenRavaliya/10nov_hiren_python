from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from q3.models import Doctor
from .serializers import DoctorSerializer


class DoctorListView(APIView):
    """
    Class-Based View for Create and List operations.
    GET  /q5/doctors/      — list all doctors
    POST /q5/doctors/      — create a new doctor
    """

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailView(APIView):
    """
    Class-Based View for Read, Update, Delete by ID.
    GET    /q5/doctors/<id>/ — retrieve one doctor
    PUT    /q5/doctors/<id>/ — full update
    PATCH  /q5/doctors/<id>/ — partial update
    DELETE /q5/doctors/<id>/ — delete
    """

    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return None

    def get(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        if not doctor:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        doctor.delete()
        return Response({'message': 'Doctor deleted'}, status=status.HTTP_204_NO_CONTENT)


# ---- HTML Views ----

def doctor_ui(request):
    """Frontend: list + add doctor form."""
    doctors = Doctor.objects.all().order_by('-created_at')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            data = {
                'name': request.POST.get('name'),
                'specialty': request.POST.get('specialty'),
                'contact_email': request.POST.get('contact_email'),
                'contact_phone': request.POST.get('contact_phone'),
                'hospital': request.POST.get('hospital', ''),
                'city': request.POST.get('city', ''),
                'available': request.POST.get('available') == 'on',
            }
            s = DoctorSerializer(data=data)
            if s.is_valid():
                s.save()
                messages.success(request, 'Doctor added!')
            else:
                messages.error(request, f'Error: {s.errors}')
        elif action == 'delete':
            pk = request.POST.get('pk')
            Doctor.objects.filter(pk=pk).delete()
            messages.success(request, 'Doctor deleted.')
        return redirect('q5_ui')
    return render(request, 'q5/doctors.html', {'doctors': doctors})


def doctor_edit_ui(request, pk):
    """Frontend: edit a single doctor."""
    doctor = get_object_or_404(Doctor, pk=pk)
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
        s = DoctorSerializer(doctor, data=data)
        if s.is_valid():
            s.save()
            messages.success(request, 'Doctor updated!')
            return redirect('q5_ui')
        else:
            messages.error(request, f'Error: {s.errors}')
    return render(request, 'q5/edit.html', {'doctor': doctor})
