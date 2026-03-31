from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.auth_home, name='q13_home'),
    path('register/', views.register_view, name='q13_register'),
    path('login/', views.login_view, name='q13_login'),
    path('logout/', views.logout_view, name='q13_logout'),
    path('dashboard/', views.dashboard, name='q13_dashboard'),
    path('profile/', views.profile_view, name='q13_profile'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='q13_auth/password_change.html', success_url='/q13/dashboard/'), name='q13_password_change'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='q13_auth/password_reset.html', success_url='/q13/reset_password_sent/'), name='q13_password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='q13_auth/password_reset_sent.html'), name='q13_password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='q13_auth/password_reset_confirm.html', success_url='/q13/reset_password_complete/'), name='q13_password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='q13_auth/password_reset_complete.html'), name='q13_password_reset_complete'),
]