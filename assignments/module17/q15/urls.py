from django.urls import path
from . import views
urlpatterns = [
    path('', views.geocode, name='q15_geocode'),
]
