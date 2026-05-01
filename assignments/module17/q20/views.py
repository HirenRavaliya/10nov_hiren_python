import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import OTPRecord

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_twilio(phone, otp):
    from twilio.rest import Client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        body=f'Your OTP for Module 17 registration is: {otp}. Valid for 10 minutes.',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )
    return msg.sid

def otp_view(request):
    step = request.session.get('otp_step', 'send')
    otp_records = OTPRecord.objects.all().order_by('-created_at')[:10]

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'send':
            phone = request.POST.get('phone', '').strip()
            otp = generate_otp()
            twilio_configured = (
                settings.TWILIO_ACCOUNT_SID and
                settings.TWILIO_ACCOUNT_SID != 'your_twilio_account_sid_here'
            )
            if not twilio_configured:
                record = OTPRecord.objects.create(phone=phone, otp=otp)
                request.session['otp_id'] = record.id
                request.session['otp_step'] = 'verify'
                messages.warning(request, f'Twilio not configured. Demo OTP: {otp} (shown for testing only)')
            else:
                try:
                    send_otp_via_twilio(phone, otp)
                    record = OTPRecord.objects.create(phone=phone, otp=otp)
                    request.session['otp_id'] = record.id
                    request.session['otp_step'] = 'verify'
                    messages.success(request, f'OTP sent to {phone}!')
                except Exception as e:
                    messages.error(request, f'Twilio error: {e}')
            return redirect('/q20/')

        elif action == 'verify':
            entered_otp = request.POST.get('otp', '').strip()
            otp_id = request.session.get('otp_id')
            try:
                record = OTPRecord.objects.get(id=otp_id)
                if record.otp == entered_otp:
                    record.verified = True
                    record.save()
                    request.session['otp_step'] = 'send'
                    request.session.pop('otp_id', None)
                    messages.success(request, '✅ OTP verified! Registration complete.')
                else:
                    messages.error(request, '❌ Invalid OTP. Please try again.')
            except OTPRecord.DoesNotExist:
                messages.error(request, 'Session expired. Please request a new OTP.')
                request.session['otp_step'] = 'send'
            return redirect('/q20/')

        elif action == 'reset':
            request.session['otp_step'] = 'send'
            request.session.pop('otp_id', None)
            return redirect('/q20/')

    return render(request, 'q20/otp.html', {
        'step': step,
        'otp_records': otp_records,
        'twilio_configured': bool(
            settings.TWILIO_ACCOUNT_SID and
            settings.TWILIO_ACCOUNT_SID != 'your_twilio_account_sid_here'
        ),
    })
