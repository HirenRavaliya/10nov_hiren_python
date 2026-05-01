from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_form, name='q4_form'),
    path('doctors/', views.add_doctor, name='q4_add_doctor'),
]
