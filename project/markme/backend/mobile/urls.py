"""
Mobile API URL Configuration — all mounted under /api/mobile/
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # ── Auth ─────────────────────────────────────────────────────────────────
    path('auth/login/',   views.MobileLoginView.as_view(),  name='mobile-login'),
    path('auth/refresh/', TokenRefreshView.as_view(),        name='mobile-token-refresh'),
    path('auth/logout/',  views.MobileLogoutView.as_view(), name='mobile-logout'),

    # ── Profile ───────────────────────────────────────────────────────────────
    path('profile/',           views.MobileProfileView.as_view(),   name='mobile-profile'),
    path('profile/fcm-token/', views.MobileFCMTokenView.as_view(),  name='mobile-fcm-token'),

    # ── Calendar ──────────────────────────────────────────────────────────────
    path('calendar/', views.CalendarView.as_view(), name='mobile-calendar'),

    # ── Attendance ────────────────────────────────────────────────────────────
    path('attendance/history/', views.MobileAttendanceHistoryView.as_view(), name='mobile-attendance-history'),
    path('attendance/report/',  views.AttendanceReportView.as_view(),         name='mobile-attendance-report'),

    # ── Analytics ─────────────────────────────────────────────────────────────
    path('analytics/', views.AnalyticsView.as_view(), name='mobile-analytics'),

    # ── Export ────────────────────────────────────────────────────────────────
    path('export/csv/', views.ExportCSVView.as_view(), name='mobile-export-csv'),
    path('export/pdf/', views.ExportPDFView.as_view(), name='mobile-export-pdf'),

    # ── Notifications ─────────────────────────────────────────────────────────
    path('notifications/',              views.MobileNotificationsView.as_view(), name='mobile-notifications'),
    path('notifications/unread-count/', views.MobileUnreadCountView.as_view(),   name='mobile-notifications-unread'),
    path('notifications/mark-read/',    views.MobileMarkReadView.as_view(),      name='mobile-notifications-mark-read'),

    # ── Leave Requests (educational only) ─────────────────────────────────────
    path('leave-requests/',           views.MobileLeaveRequestListCreateView.as_view(), name='mobile-leave-list'),
    path('leave-requests/<uuid:pk>/', views.MobileLeaveRequestDetailView.as_view(),    name='mobile-leave-detail'),
]
