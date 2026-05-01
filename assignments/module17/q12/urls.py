from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'doctors', views.DoctorViewSet, basename='q12_doctor')

urlpatterns = [
    path('', views.crud_dashboard, name='q12_ui'),
    path('', include(router.urls)),
]
