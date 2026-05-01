from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagination_ui, name='q7_ui'),
    path('doctors/', views.DoctorPaginatedList.as_view(), name='q7_doctor_list'),
]
