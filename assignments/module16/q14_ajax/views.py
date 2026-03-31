import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from q6_doctor.models import Doctor

def index(request):
    return render(request, 'q14_ajax/index.html', {
        'specialties': Doctor.SPECIALTY_CHOICES
    })

@csrf_exempt
def items_api(request):
    if request.method == 'GET':
        doctors = list(Doctor.objects.values('id', 'name', 'specialty', 'hospital', 'city', 'phone', 'email', 'created_at'))
        for d in doctors:
            d['created_at'] = d['created_at'].strftime('%b %d, %Y') if d['created_at'] else ''
        return JsonResponse({'doctors': doctors})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            doctor = Doctor.objects.create(
                name=data.get('name'),
                specialty=data.get('specialty'),
                hospital=data.get('hospital'),
                city=data.get('city'),
                phone=data.get('phone'),
                email=data.get('email')
            )
            return JsonResponse({
                'id': doctor.id,
                'name': doctor.name,
                'specialty': doctor.specialty,
                'created_at': doctor.created_at.strftime('%b %d, %Y')
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def item_api(request, pk):
    try:
        doctor = Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': doctor.id,
            'name': doctor.name,
            'specialty': doctor.specialty,
            'hospital': doctor.hospital,
            'city': doctor.city,
            'phone': doctor.phone,
            'email': doctor.email
        })

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            doctor.name = data.get('name', doctor.name)
            doctor.specialty = data.get('specialty', doctor.specialty)
            doctor.hospital = data.get('hospital', doctor.hospital)
            doctor.city = data.get('city', doctor.city)
            doctor.phone = data.get('phone', doctor.phone)
            doctor.email = data.get('email', doctor.email)
            doctor.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        doctor.delete()
        return JsonResponse({'deleted': True})