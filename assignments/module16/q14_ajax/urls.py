from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='q14_index'),
    path('api/items/', views.items_api, name='q14_api_list'),
    path('api/items/<int:pk>/', views.item_api, name='q14_api_item'),
]