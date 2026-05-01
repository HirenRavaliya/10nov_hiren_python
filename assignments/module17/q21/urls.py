from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_home, name='q21_booking'),
    path('book/', views.book_appointment, name='q21_book'),
    path('success/<int:appointment_id>/', views.payment_success, name='q21_success'),
    path('cancel/', views.payment_cancel, name='q21_cancel'),
]
