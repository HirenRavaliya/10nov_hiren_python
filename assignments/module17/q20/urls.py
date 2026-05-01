from django.urls import path
from . import views
urlpatterns = [
    path('', views.otp_view, name='q20_otp'),
]
