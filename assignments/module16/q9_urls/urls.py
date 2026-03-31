from django.urls import path
from . import views

app_name = "doctor_finder"

urlpatterns = [

    path("", views.home, name="home"),


    path("profile/<int:doctor_id>/", views.profile, name="profile"),


    path("contact/", views.contact, name="contact"),
]