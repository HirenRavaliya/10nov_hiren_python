from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'doctors', views.DoctorViewSet, basename='q6_doctor')

urlpatterns = [
    path('', views.router_ui, name='q6_ui'),
    path('', include(router.urls)),
]
