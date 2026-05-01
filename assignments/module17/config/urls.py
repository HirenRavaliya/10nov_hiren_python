"""URL configuration for config project."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Q1 — Joke API
    path('q1/', include('q1.urls')),
    # Q2 — Setup documentation
    path('q2/', include('q2.urls')),
    # Q3 — Doctor serializer
    path('q3/', include('q3.urls')),
    # Q4 — POST add doctor
    path('q4/', include('q4.urls')),
    # Q5 — Class-based views CRUD
    path('q5/', include('q5.urls')),
    # Q6 — URL routing CRUD
    path('q6/', include('q6.urls')),
    # Q7 — Pagination
    path('q7/', include('q7.urls')),
    # Q8 — SQLite settings
    path('q8/', include('q8.urls')),
    # Q9 — doctor_finder setup
    path('q9/', include('q9.urls')),
    # Q10 — Social auth + OTP (placeholder)
    path('q10/', include('q10.urls')),
    # Q11 — RESTful API
    path('q11/', include('q11.urls')),
    # Q12 — Full CRUD API
    path('q12/', include('q12.urls')),
    # Q13 — Token authentication
    path('q13/', include('q13.urls')),
    # Q14 — OpenWeatherMap
    path('q14/', include('q14.urls')),
    # Q15 — Google Maps Geocoding
    path('q15/', include('q15.urls')),
    # Q16 — GitHub API
    path('q16/', include('q16.urls')),
    # Q17 — Twitter API (placeholder)
    path('q17/', include('q17.urls')),
    # Q18 — REST Countries
    path('q18/', include('q18.urls')),
    # Q19 — SendGrid email
    path('q19/', include('q19.urls')),
    # Q20 — Twilio OTP
    path('q20/', include('q20.urls')),
    # Q21 — Stripe payments
    path('q21/', include('q21.urls')),
    # Q22 — Google Maps doctor locations
    path('q22/', include('q22.urls')),
]
