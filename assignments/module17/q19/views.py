from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Registration
import sendgrid
from sendgrid.helpers.mail import Mail

def send_confirmation_email(to_email, name):
    """Send confirmation email via SendGrid."""
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    message = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject='Registration Confirmed — Module 17 Django App',
        html_content=f"""
        <h2>Welcome, {name}!</h2>
        <p>Your registration has been confirmed successfully.</p>
        <p>Thank you for joining our platform.</p>
        <br>
        <p>Best regards,<br>Module 17 Team</p>
        """
    )
    response = sg.send(message)
    return response.status_code

def register(request):
    registrations = Registration.objects.all().order_by('-registered_at')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        if not name or not email:
            messages.error(request, 'Name and email are required.')
            return redirect('/q19/')
        if Registration.objects.filter(email=email).exists():
            messages.warning(request, f'{email} is already registered.')
            return redirect('/q19/')
        api_key = settings.SENDGRID_API_KEY
        if not api_key or api_key == 'your_sendgrid_api_key_here':
            reg = Registration.objects.create(name=name, email=email, email_sent=False)
            messages.warning(request, f'{name} registered! (SendGrid not configured — email not sent. Add SENDGRID_API_KEY to .env)')
        else:
            try:
                status_code = send_confirmation_email(email, name)
                email_sent = status_code == 202
                reg = Registration.objects.create(name=name, email=email, email_sent=email_sent)
                if email_sent:
                    messages.success(request, f'✅ {name} registered! Confirmation email sent to {email}.')
                else:
                    messages.warning(request, f'{name} registered but email failed (status: {status_code}).')
            except Exception as e:
                reg = Registration.objects.create(name=name, email=email, email_sent=False)
                messages.error(request, f'{name} registered but email error: {e}')
        return redirect('/q19/')
    return render(request, 'q19/register.html', {'registrations': registrations})
