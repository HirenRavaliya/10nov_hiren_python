from django.urls import path
from . import views
urlpatterns = [
    path('', views.item_list, name='q12_list'),
    path('add/', views.item_add, name='q12_add'),
    path('edit/<int:pk>/', views.item_edit, name='q12_edit'),
    path('delete/<int:pk>/', views.item_delete, name='q12_delete'),
]