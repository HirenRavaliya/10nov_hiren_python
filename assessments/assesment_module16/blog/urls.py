from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('post/<slug:slug>/like/', views.like_toggle, name='like_toggle'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
