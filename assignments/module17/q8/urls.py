from django.urls import path
from . import views

urlpatterns = [
    path('', views.sqlite_ui, name='q8_ui'),
    path('doctors/', views.DoctorList.as_view(), name='q8_doctor_list'),
    path('doctors/<int:pk>/', views.DoctorDetail.as_view(), name='q8_doctor_detail'),
]
