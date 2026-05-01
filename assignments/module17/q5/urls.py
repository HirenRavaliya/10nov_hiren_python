from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_ui, name='q5_ui'),
    path('edit/<int:pk>/', views.doctor_edit_ui, name='q5_edit'),
    path('doctors/', views.DoctorListView.as_view(), name='q5_doctor_list'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='q5_doctor_detail'),
]
