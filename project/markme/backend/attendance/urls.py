from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'logs', views.AttendanceLogViewSet, basename='attendance-log')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'leave-requests', views.LeaveRequestViewSet, basename='leave-request')

urlpatterns = [
    path('', include(router.urls)),

    # AI face scan
    path('scan/', views.FaceScanView.as_view(), name='face-scan'),

    # Manual attendance
    path('manual/', views.ManualAttendanceView.as_view(), name='manual-attendance'),

    # Dashboard & analytics
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),

    # Mobile app: student's own history + leaves
    path('my-history/', views.MyAttendanceHistoryView.as_view(), name='my-history'),
    path('my-notifications/', views.MyNotificationsView.as_view(), name='my-notifications'),
    path('my-leaves/', views.MyLeaveRequestsView.as_view(), name='my-leaves'),
    path('my-leaves/<uuid:pk>/', views.MyLeaveRequestDetailView.as_view(), name='my-leave-detail'),
]
