"""Root URL Configuration for Hajri Hub Backend"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth endpoints (JWT)
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # App APIs
    path('api/accounts/',  include('accounts.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/mobile/',    include('mobile.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
