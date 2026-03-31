from django.urls import path
from . import views

app_name = "social_auth"

from django.shortcuts import redirect

urlpatterns = [

    path("",           lambda request: redirect("social_auth:login")),


    path("login/",     views.login_view, name="login"),


    path("dashboard/", views.dashboard,  name="dashboard"),


    path("logout/",    views.logout_view, name="logout"),
]