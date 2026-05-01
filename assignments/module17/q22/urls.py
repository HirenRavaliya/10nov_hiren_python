from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_map, name='q22_map'),
    path('api/', views.doctor_locations_api, name='q22_api'),
]
