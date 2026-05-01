from django.urls import path
from . import views

urlpatterns = [
    path('', views.setup_guide, name='q2_setup'),
]
