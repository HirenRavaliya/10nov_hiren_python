from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_ui, name='q3_ui'),
    path('doctors/', views.doctor_list, name='q3_doctor_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='q3_doctor_detail'),
]
