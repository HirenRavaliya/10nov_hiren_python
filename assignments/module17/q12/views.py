from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from q3.models import Doctor
from .serializers import DoctorSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    """Complete CRUD API for doctor profiles."""
    queryset = Doctor.objects.all().order_by('-created_at')
    serializer_class = DoctorSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Custom action: /q12/doctors/available/ — only available doctors"""
        doctors = Doctor.objects.filter(available=True)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

def crud_dashboard(request):
    doctors = Doctor.objects.all().order_by('-created_at')
    edit_doctor = None
    edit_id = request.GET.get('edit')
    if edit_id:
        edit_doctor = get_object_or_404(Doctor, pk=edit_id)

    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        if action_type == 'create':
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
                messages.success(request, 'Doctor created!')
            else:
                messages.error(request, str(s.errors))
        elif action_type == 'update':
            pk = request.POST.get('pk')
            doc = get_object_or_404(Doctor, pk=pk)
            data = {
                'name': request.POST.get('name'),
                'specialty': request.POST.get('specialty'),
                'contact_email': request.POST.get('contact_email'),
                'contact_phone': request.POST.get('contact_phone'),
                'hospital': request.POST.get('hospital', ''),
                'city': request.POST.get('city', ''),
                'available': request.POST.get('available') == 'on',
            }
            s = DoctorSerializer(doc, data=data)
            if s.is_valid():
                s.save()
                messages.success(request, 'Doctor updated!')
            else:
                messages.error(request, str(s.errors))
        elif action_type == 'delete':
            pk = request.POST.get('pk')
            Doctor.objects.filter(pk=pk).delete()
            messages.success(request, 'Doctor deleted!')
        return redirect('/q12/')
    return render(request, 'q12/crud.html', {'doctors': doctors, 'edit_doctor': edit_doctor})
