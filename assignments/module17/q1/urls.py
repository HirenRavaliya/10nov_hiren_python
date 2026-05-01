from django.urls import path
from . import views

urlpatterns = [
    path('', views.fetch_joke, name='q1_joke'),
]
