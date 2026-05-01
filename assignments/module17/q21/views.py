import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Appointment

stripe.api_key = settings.STRIPE_SECRET_KEY

DOCTOR_FEES = [
    {'name': 'Dr. Sharma', 'specialty': 'Cardiologist', 'fee': 1500},
    {'name': 'Dr. Patel', 'specialty': 'Dermatologist', 'fee': 800},
    {'name': 'Dr. Mehta', 'specialty': 'Neurologist', 'fee': 2000},
    {'name': 'Dr. Iyer', 'specialty': 'Orthopedic', 'fee': 1200},
]

def booking_home(request):
    appointments = Appointment.objects.all().order_by('-created_at')
    stripe_configured = bool(
        settings.STRIPE_SECRET_KEY and
        settings.STRIPE_SECRET_KEY != 'your_stripe_secret_key_here'
    )
    return render(request, 'q21/booking.html', {
        'doctors': DOCTOR_FEES,
        'appointments': appointments,
        'stripe_pk': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_configured': stripe_configured,
    })

def book_appointment(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        patient_email = request.POST.get('patient_email')
        doctor_name = request.POST.get('doctor_name')
        doctor_specialty = request.POST.get('doctor_specialty')
        appointment_date = request.POST.get('appointment_date')
        amount = int(request.POST.get('amount', 500))

        appointment = Appointment.objects.create(
            patient_name=patient_name,
            patient_email=patient_email,
            doctor_name=doctor_name,
            doctor_specialty=doctor_specialty,
            appointment_date=appointment_date,
            amount=amount,
            status='pending',
        )

        if not settings.STRIPE_SECRET_KEY or settings.STRIPE_SECRET_KEY == 'your_stripe_secret_key_here':
            appointment.status = 'paid'
            appointment.stripe_session_id = 'DEMO_SESSION'
            appointment.save()
            messages.success(request, f'✅ Demo booking confirmed for {patient_name} with {doctor_name}! (Stripe not configured)')
            return redirect('/q21/')

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f'Appointment with {doctor_name}',
                            'description': f'{doctor_specialty} consultation on {appointment_date}',
                        },
                        'unit_amount': amount * 100,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'http://localhost:8000/q21/success/{appointment.id}/',
                cancel_url='http://localhost:8000/q21/cancel/',
                customer_email=patient_email,
            )
            appointment.stripe_session_id = session.id
            appointment.save()
            return redirect(session.url)
        except Exception as e:
            appointment.status = 'failed'
            appointment.save()
            messages.error(request, f'Stripe error: {e}')
            return redirect('/q21/')
    return redirect('/q21/')

def payment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'paid'
    appointment.save()
    return render(request, 'q21/success.html', {'appointment': appointment})

def payment_cancel(request):
    return render(request, 'q21/cancel.html')
