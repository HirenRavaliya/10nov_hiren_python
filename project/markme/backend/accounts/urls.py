from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'teachers', views.TeacherViewSet, basename='teacher')
router.register(r'organizations', views.OrganizationViewSet, basename='organization')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('me/', views.MeView.as_view(), name='me'),
    path('me/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('me/fcm-token/', views.UpdateFCMTokenView.as_view(), name='update-fcm-token'),
    path('students/<uuid:pk>/enroll-face/', views.EnrollFaceView.as_view(), name='enroll-face'),
]
