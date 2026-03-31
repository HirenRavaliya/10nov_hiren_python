from django.urls import path
from . import views

app_name = "doctor_map"

urlpatterns = [
    # Full-page interactive map      →  /map/
    path("", views.map_home, name="map_home"),

    # Doctor detail + mini-map       →  /map/doctor/1/
    path("doctor/<int:doctor_id>/", views.doctor_detail, name="doctor_detail"),

    # About / how it works           →  /map/about/
    path("about/", views.about, name="about"),
]
