from django.shortcuts import render, get_object_or_404, redirect
from .models import Doctor
from django import forms

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'hospital', 'city', 'experience_years', 'phone', 'email', 'fee', 'is_available']
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in ['name', 'hospital', 'city', 'phone', 'email']}

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'q6_doctor/list.html', {'doctors': doctors})

def doctor_add(request):
    form = DoctorForm()
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('q6_list')
    return render(request, 'q6_doctor/add.html', {'form': form})

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'q6_doctor/detail.html', {'doctor': doctor})