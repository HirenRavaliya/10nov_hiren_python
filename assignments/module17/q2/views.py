from django.shortcuts import render


def setup_guide(request):
    packages = [
        {'name': 'django', 'version': '5.x', 'purpose': 'Core web framework'},
        {'name': 'djangorestframework', 'version': '3.x', 'purpose': 'REST API toolkit for Django'},
        {'name': 'requests', 'version': '2.x', 'purpose': 'HTTP library for calling external APIs'},
        {'name': 'python-dotenv', 'version': '1.x', 'purpose': 'Load environment variables from .env file'},
        {'name': 'sendgrid', 'version': '6.x', 'purpose': 'SendGrid email API client'},
        {'name': 'twilio', 'version': '9.x', 'purpose': 'Twilio SMS/OTP API client'},
        {'name': 'stripe', 'version': '15.x', 'purpose': 'Stripe payment integration'},
        {'name': 'django-allauth', 'version': '65.x', 'purpose': 'Social authentication (Google login)'},
        {'name': 'djangorestframework-simplejwt', 'version': '5.x', 'purpose': 'JWT token authentication'},
        {'name': 'Pillow', 'version': '10.x', 'purpose': 'Image processing'},
    ]
    steps = [
        ('Create virtual environment', 'python3 -m venv venv'),
        ('Activate venv (Mac/Linux)', 'source venv/bin/activate'),
        ('Activate venv (Windows)', r'venv\Scripts\activate'),
        ('Install packages', 'pip install django djangorestframework requests python-dotenv sendgrid twilio stripe django-allauth Pillow'),
        ('Create Django project', 'django-admin startproject config .'),
        ('Create an app', 'python manage.py startapp q1'),
        ('Run migrations', 'python manage.py migrate'),
        ('Start development server', 'python manage.py runserver'),
    ]
    return render(request, 'q2/setup.html', {'packages': packages, 'steps': steps})
