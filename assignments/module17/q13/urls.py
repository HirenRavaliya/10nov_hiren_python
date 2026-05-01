from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_ui, name='q13_ui'),
    path('token/', views.CustomAuthToken.as_view(), name='q13_token'),
    path('doctors/', views.DoctorProtectedList.as_view(), name='q13_doctor_list'),
    path('doctors/<int:pk>/', views.DoctorProtectedDetail.as_view(), name='q13_doctor_detail'),
    path('public/doctors/', views.DoctorPublicList.as_view(), name='q13_public_list'),
]
