from django.urls import path
from . import views

urlpatterns = [
    path('', views.restful_ui, name='q11_ui'),
    path('doctors/', views.DoctorList.as_view(), name='q11_doctor_list'),
    path('doctors/<int:pk>/', views.DoctorDetail.as_view(), name='q11_doctor_detail'),
]
