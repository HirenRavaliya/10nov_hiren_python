from django.urls import path
from . import views
urlpatterns = [
    path('', views.github_repos, name='q16_github'),
]
