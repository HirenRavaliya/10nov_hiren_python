from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from q6_doctor.models import Doctor

def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            Doctor.objects.create(
                name=request.POST.get('name'),
                specialty=request.POST.get('specialty'),
                hospital=request.POST.get('hospital'),
                city=request.POST.get('city'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email')
            )
        elif action == 'edit':
            doc_id = request.POST.get('doc_id')
            doc = get_object_or_404(Doctor, id=doc_id)
            doc.name = request.POST.get('name')
            doc.specialty = request.POST.get('specialty')
            doc.hospital = request.POST.get('hospital')
            doc.city = request.POST.get('city')
            doc.phone = request.POST.get('phone')
            doc.email = request.POST.get('email')
            doc.save()
        elif action == 'delete':
            doc_id = request.POST.get('doc_id')
            Doctor.objects.filter(id=doc_id).delete()
        return redirect('q11_index')

    status = {'connected': False, 'db_name': '', 'error': ''}
    try:

        if connection.vendor == 'mysql':
            with connection.cursor() as cursor:
                cursor.execute("SELECT DATABASE()")
                status['db_name'] = cursor.fetchone()[0]
        else:

            db_path = connection.settings_dict['NAME']
            import os
            status['db_name'] = os.path.basename(str(db_path))

        status['connected'] = True
    except Exception as e:
        status['error'] = str(e)

    doctors = Doctor.objects.all()
    editing_doctor = None
    edit_id = request.GET.get('edit_id')
    if edit_id:
        editing_doctor = Doctor.objects.filter(id=edit_id).first()

    return render(request, 'q11_db/index.html', {
        'status': status,
        'doctors': doctors,
        'specialties': Doctor.SPECIALTY_CHOICES,
        'editing_doctor': editing_doctor
    })