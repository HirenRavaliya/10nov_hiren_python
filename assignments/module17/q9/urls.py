from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'doctors', views.DoctorViewSet, basename='q9_doctor')

urlpatterns = [
    path('', views.doctor_finder_ui, name='q9_ui'),
    path('api/', include(router.urls)),
]
