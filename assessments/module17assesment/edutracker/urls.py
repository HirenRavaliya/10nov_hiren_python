"""
EduTracker Solutions – Root URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import api_root

urlpatterns = [
    # API root – lists all endpoints
    path('', api_root, name='api_root'),

    # Django admin
    path('admin/', admin.site.urls),

    # JWT auth endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App-level routes
    path('api/students/', include('students.urls')),
    path('api/courses/', include('courses.urls')),

    # DRF browsable API login/logout (adds the "Log in" button)
    path('api-auth/', include('rest_framework.urls')),
]
