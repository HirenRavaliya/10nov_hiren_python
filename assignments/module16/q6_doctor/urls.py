from django.urls import path
from . import views
urlpatterns = [
    path('', views.doctor_list, name='q6_list'),
    path('add/', views.doctor_add, name='q6_add'),
    path('<int:pk>/', views.doctor_detail, name='q6_detail'),
]