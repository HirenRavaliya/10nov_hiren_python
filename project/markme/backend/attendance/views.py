"""
Attendance Views — the heart of the system.

Key endpoints:
  POST /api/attendance/scan/          AI face scan → mark attendance
  POST /api/attendance/manual/        Manual mark attendance
  GET  /api/attendance/logs/          List/filter logs (admin/teacher)
  GET  /api/attendance/my-history/    Student's own attendance (mobile)
  GET  /api/attendance/notifications/ Student's own notifications (mobile)
  GET  /api/attendance/dashboard/     Stats for the dashboard
  GET  /api/attendance/analytics/     30-day chart data
"""
import logging
from datetime import date, timedelta
from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Q
from rest_framework import viewsets, generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import Student
from accounts.permissions import IsAdminOrTeacher
from .models import AttendanceLog, Notification, LeaveRequest
from .serializers import (
    AttendanceLogSerializer,
    ManualAttendanceSerializer,
    FaceScanSerializer,
    NotificationSerializer,
    AttendanceSummarySerializer,
    LeaveRequestSerializer,
    LeaveRequestCreateSerializer,
    LeaveRequestReviewSerializer,
)
from .face_engine import identify_face_from_image, identify_face_from_base64
from .notifications import notify_attendance_marked

logger = logging.getLogger(__name__)


# ── AI Face Scan ──────────────────────────────────────────────────────────────

class FaceScanView(APIView):
    """
    POST /api/attendance/scan/

    Accepts an image (multipart file OR base64 string), runs the AI face
    recognition engine, and marks attendance for the matched student.

    Used by the browser-based Live Scanner page.
    Returns recognized student info, confidence score, and the attendance log.
    """
    permission_classes = [IsAdminOrTeacher]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        serializer = FaceScanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tolerance = float(request.data.get('tolerance', settings.FACE_RECOGNITION_TOLERANCE))

        # Identify face
        if serializer.validated_data.get('image'):
            result = identify_face_from_image(
                serializer.validated_data['image'],
                tolerance=tolerance
            )
        else:
            result = identify_face_from_base64(
                serializer.validated_data['image_base64'],
                tolerance=tolerance
            )

        if not result['face_found']:
            return Response({
                'matched': False,
                'message': result['message'],
            }, status=status.HTTP_400_BAD_REQUEST)

        if not result['matched']:
            return Response({
                'matched': False,
                'confidence': result['confidence'],
                'message': result['message'],
            }, status=status.HTTP_200_OK)

        # We have a match — mark attendance
        student = result['student']
        today = timezone.localdate()

        # Check for duplicate today
        existing = AttendanceLog.objects.filter(student=student, date=today).first()
        if existing:
            return Response({
                'matched': True,
                'already_marked': True,
                'student_name': student.user.full_name,
                'confidence': result['confidence'],
                'attendance': AttendanceLogSerializer(existing, context={'request': request}).data,
                'message': f'Attendance already marked for {student.user.full_name} today.',
            }, status=status.HTTP_200_OK)

        # Create new attendance record
        log = AttendanceLog.objects.create(
            student=student,
            status=AttendanceLog.PRESENT,
            method=AttendanceLog.METHOD_FACE,
            confidence=result['confidence'],
        )

        # Fire push notification (async in production, sync here for dev)
        try:
            notify_attendance_marked(student, log)
        except Exception as e:
            logger.error(f'Notification error: {e}')

        return Response({
            'matched': True,
            'already_marked': False,
            'student_name': student.user.full_name,
            'confidence': result['confidence'],
            'attendance': AttendanceLogSerializer(log, context={'request': request}).data,
            'message': result['message'],
        }, status=status.HTTP_201_CREATED)


# ── Manual Attendance ─────────────────────────────────────────────────────────

class ManualAttendanceView(APIView):
    """
    POST /api/attendance/manual/
    Mark attendance manually for a student (admin/teacher only).
    """
    permission_classes = [IsAdminOrTeacher]
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = ManualAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            student = Student.objects.get(pk=data['student_id'])
        except Student.DoesNotExist:
            return Response({'detail': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()
        log, created = AttendanceLog.objects.get_or_create(
            student=student,
            date=today,
            defaults={
                'status': data['status'],
                'method': AttendanceLog.METHOD_MANUAL,
                'notes': data.get('notes', ''),
            }
        )

        if not created:
            # Update existing
            log.status = data['status']
            log.method = AttendanceLog.METHOD_MANUAL
            log.notes = data.get('notes', '')
            log.save()

        if created and data['status'] == AttendanceLog.PRESENT:
            try:
                notify_attendance_marked(student, log)
            except Exception as e:
                logger.error(f'Notification error: {e}')

        return Response({
            'created': created,
            'attendance': AttendanceLogSerializer(log, context={'request': request}).data,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# ── Attendance Logs (Admin) ───────────────────────────────────────────────────

class AttendanceLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/attendance/logs/
    GET /api/attendance/logs/<id>/
    Filterable by student, date, status, method.
    """
    queryset = AttendanceLog.objects.select_related('student__user').all()
    serializer_class = AttendanceLogSerializer
    permission_classes = [IsAdminOrTeacher]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'date', 'status', 'method']
    search_fields = ['student__user__full_name']
    ordering_fields = ['timestamp', 'date', 'student__user__full_name']
    ordering = ['-timestamp']


# ── Mobile: Student's own history ────────────────────────────────────────────

class MyAttendanceHistoryView(generics.ListAPIView):
    """
    GET /api/attendance/my-history/
    Returns the authenticated student's full attendance history.
    Used by the mobile app.
    """
    serializer_class = AttendanceLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            student = user.student_profile
            return AttendanceLog.objects.filter(student=student).order_by('-timestamp')
        except AttributeError:
            return AttendanceLog.objects.none()


class MyNotificationsView(generics.ListAPIView):
    """
    GET /api/attendance/my-notifications/
    Returns all notifications for the logged-in student.
    Used by the mobile app.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            student = user.student_profile
            return Notification.objects.filter(student=student).order_by('-created_at')
        except AttributeError:
            return Notification.objects.none()


# ── Notification Logs (Admin) ─────────────────────────────────────────────────

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/attendance/notifications/
    Admin/teacher can see all notification logs.
    """
    queryset = Notification.objects.select_related('student__user').all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrTeacher]
    filterset_fields = ['student', 'status', 'notification_type']
    ordering = ['-created_at']


# ── Dashboard Stats ───────────────────────────────────────────────────────────

class DashboardView(APIView):
    """
    GET /api/attendance/dashboard/
    Returns live stats for the admin dashboard:
    - total students, present today, absent today, attendance rate
    - recent logs
    """
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        today = timezone.localdate()
        total_students = Student.objects.count()
        today_logs = AttendanceLog.objects.filter(date=today)
        present_today = today_logs.filter(status='PRESENT').count()
        absent_today = total_students - present_today
        rate = round((present_today / total_students * 100), 1) if total_students else 0

        recent_logs = AttendanceLog.objects.select_related('student__user').order_by('-timestamp')[:10]

        return Response({
            'today': str(today),
            'total_students': total_students,
            'present_today': present_today,
            'absent_today': absent_today,
            'attendance_rate': rate,
            'recent_logs': AttendanceLogSerializer(recent_logs, many=True, context={'request': request}).data,
        })


class AnalyticsView(APIView):
    """
    GET /api/attendance/analytics/?days=30&student_id=<uuid>
    Returns daily attendance counts for the past N days.
    """
    permission_classes = [IsAdminOrTeacher]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        student_id = request.query_params.get('student_id')
        today = timezone.localdate()

        data = []
        for i in range(days - 1, -1, -1):
            day = today - timedelta(days=i)
            qs = AttendanceLog.objects.filter(date=day, status='PRESENT')
            if student_id:
                qs = qs.filter(student__id=student_id)
            data.append({
                'date': str(day),
                'date_display': day.strftime('%d %b'),
                'count': qs.count(),
            })

        total_students = Student.objects.count()
        return Response({
            'days': days,
            'total_students': total_students,
            'chart_data': data,
        })


# ── Leave Requests ────────────────────────────────────────────────────────────

class LeaveRequestViewSet(viewsets.ModelViewSet):
    """
    Admin/Teacher: full CRUD + approve/reject action.
    GET    /api/attendance/leave-requests/
    GET    /api/attendance/leave-requests/<id>/
    POST   /api/attendance/leave-requests/<id>/review/  {action, review_note}
    DELETE /api/attendance/leave-requests/<id>/
    """
    queryset = LeaveRequest.objects.select_related('student__user', 'reviewed_by').all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAdminOrTeacher]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'reason', 'student']
    ordering = ['-created_at']
    http_method_names = ['get', 'delete', 'head', 'options']

    from rest_framework.decorators import action as drf_action

    @drf_action(detail=True, methods=['post'], url_path='review')
    def review(self, request, pk=None):
        """Approve or reject a leave request."""
        leave = self.get_object()
        serializer = LeaveRequestReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data['action']
        note   = serializer.validated_data.get('review_note', '')

        if action == 'approve':
            leave.status = LeaveRequest.STATUS_APPROVED
        else:
            leave.status = LeaveRequest.STATUS_REJECTED

        leave.reviewed_by = request.user
        leave.review_note = note
        leave.reviewed_at = timezone.now()
        leave.save()

        # Notify student
        try:
            from .notifications import send_push_notification
            from attendance.models import Notification as Notif
            title = '✅ Leave Approved' if action == 'approve' else '❌ Leave Rejected'
            body  = (
                f'Your leave request ({leave.start_date} → {leave.end_date}) '
                f'has been {leave.get_status_display().lower()}.'
                + (f' Note: {note}' if note else '')
            )
            Notif.objects.create(
                student=leave.student,
                notification_type='ALERT',
                title=title,
                message=body,
                status='PENDING',
            )
            if leave.student.user.fcm_token:
                send_push_notification(leave.student.user.fcm_token, title, body)
        except Exception as e:
            logger.warning(f'Leave notification error: {e}')

        return Response(
            LeaveRequestSerializer(leave, context={'request': request}).data,
            status=status.HTTP_200_OK
        )


class MyLeaveRequestsView(generics.ListCreateAPIView):
    """
    Mobile API — Student submits and views their own leave requests.
    GET  /api/attendance/my-leaves/
    POST /api/attendance/my-leaves/   {reason, description, start_date, end_date, proof_doc}
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LeaveRequestCreateSerializer
        return LeaveRequestSerializer

    def get_queryset(self):
        try:
            return LeaveRequest.objects.filter(
                student=self.request.user.student_profile
            ).order_by('-created_at')
        except AttributeError:
            return LeaveRequest.objects.none()

    def perform_create(self, serializer):
        try:
            student = self.request.user.student_profile
        except AttributeError:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only student accounts can submit leave requests.')
        serializer.save(student=student)


class MyLeaveRequestDetailView(generics.RetrieveDestroyAPIView):
    """
    Mobile API — Student views or withdraws a single leave request.
    GET    /api/attendance/my-leaves/<id>/
    DELETE /api/attendance/my-leaves/<id>/   (only if still PENDING)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LeaveRequestSerializer

    def get_queryset(self):
        try:
            return LeaveRequest.objects.filter(student=self.request.user.student_profile)
        except AttributeError:
            return LeaveRequest.objects.none()

    def destroy(self, request, *args, **kwargs):
        leave = self.get_object()
        if leave.status != LeaveRequest.STATUS_PENDING:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Only pending requests can be withdrawn.')
        return super().destroy(request, *args, **kwargs)
