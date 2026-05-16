"""
Mobile API Views — /api/mobile/
"""
import csv
import logging
from datetime import date, timedelta
from calendar import monthrange

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils import timezone

from rest_framework import generics, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from attendance.models import AttendanceLog, Notification, LeaveRequest
from .serializers import (
    MobileTokenObtainPairSerializer,
    MobileProfileSerializer,
    FCMTokenUpdateSerializer,
    CalendarDaySerializer,
    CalendarStatsSerializer,
    AttendanceReportSerializer,
    AnalyticsSerializer,
    MobileNotificationSerializer,
    MarkNotificationsReadSerializer,
    MobileLeaveRequestSerializer,
    MobileLeaveRequestCreateSerializer,
)
from .permissions import IsEducationalOrg

User = get_user_model()
logger = logging.getLogger(__name__)


# ── helpers ───────────────────────────────────────────────────────────────────

def _get_student(user):
    try:
        return user.student_profile
    except Exception:
        return None


def _build_calendar_data(student, year, month):
    """Returns (days_list, stats_dict) for a given month."""
    _, days_in_month = monthrange(year, month)
    month_start = date(year, month, 1)
    month_end   = date(year, month, days_in_month)
    today       = timezone.localdate()

    logs = AttendanceLog.objects.filter(
        student=student, date__gte=month_start, date__lte=month_end
    )
    leaves = LeaveRequest.objects.filter(
        student=student,
        status__in=['PENDING', 'APPROVED'],
        start_date__lte=month_end,
        end_date__gte=month_start,
    )

    logs_map = {l.date: l for l in logs}
    leave_dates = set()
    for lr in leaves:
        d = max(lr.start_date, month_start)
        while d <= min(lr.end_date, month_end):
            leave_dates.add(d)
            d += timedelta(days=1)

    days = []
    check_in_times = []
    for i in range(days_in_month):
        d = month_start + timedelta(days=i)
        log = logs_map.get(d)
        is_leave = d in leave_dates

        if log:
            s = log.status
            time_in = log.timestamp.strftime('%I:%M %p')
            check_in_times.append(log.timestamp.hour * 60 + log.timestamp.minute)
        elif is_leave:
            s = 'LEAVE'
            time_in = None
        else:
            s = 'ABSENT' if d <= today else 'NONE'
            time_in = None

        days.append({
            'date': str(d), 'day': d.day, 'weekday': d.strftime('%a'),
            'status': s, 'time_in': time_in,
            'is_leave': is_leave, 'is_today': (d == today),
        })

    present = sum(1 for x in days if x['status'] == 'PRESENT')
    late    = sum(1 for x in days if x['status'] == 'LATE')
    absent  = sum(1 for x in days if x['status'] == 'ABSENT')
    leave   = sum(1 for x in days if x['status'] == 'LEAVE')
    total_counted = present + late + absent
    rate = round(((present + late) / total_counted * 100), 1) if total_counted else 0.0

    avg_ci = None
    if check_in_times:
        avg_min = sum(check_in_times) // len(check_in_times)
        h, m = divmod(avg_min, 60)
        avg_ci = f"{h % 12 or 12}:{m:02d} {'AM' if h < 12 else 'PM'}"

    stats = {
        'attendance_rate': f'{rate}%',
        'avg_check_in': avg_ci,
        'days_absent': absent,
        'leave_days': leave,
    }
    return days, stats


# ══════════════════════════════════════════════════════════════════════════════
# Auth
# ══════════════════════════════════════════════════════════════════════════════

class MobileLoginView(TokenObtainPairView):
    """POST /api/mobile/auth/login/"""
    serializer_class  = MobileTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class MobileLogoutView(APIView):
    """POST /api/mobile/auth/logout/  — blacklists the refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.data.get('refresh')
        if not token:
            return Response({'detail': 'Refresh token required.'}, status=400)
        try:
            RefreshToken(token).blacklist()
        except TokenError as e:
            return Response({'detail': str(e)}, status=400)
        return Response({'detail': 'Logged out successfully.'})


# ══════════════════════════════════════════════════════════════════════════════
# Profile
# ══════════════════════════════════════════════════════════════════════════════

class MobileProfileView(generics.RetrieveUpdateAPIView):
    """GET / PATCH /api/mobile/profile/"""
    serializer_class   = MobileProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser, JSONParser]
    http_method_names  = ['get', 'patch', 'head', 'options']

    def get_object(self):
        return self.request.user


class MobileFCMTokenView(APIView):
    """POST /api/mobile/profile/fcm-token/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        s = FCMTokenUpdateSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        request.user.fcm_token = s.validated_data['fcm_token']
        request.user.save(update_fields=['fcm_token'])
        return Response({'detail': 'FCM token updated.'})


# ══════════════════════════════════════════════════════════════════════════════
# Calendar
# ══════════════════════════════════════════════════════════════════════════════

class CalendarView(APIView):
    """
    GET /api/mobile/calendar/?month=4&year=2026
    Returns per-day attendance status + 4 stat cards for the calendar screen.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        student = _get_student(request.user)
        if not student:
            return Response({'detail': 'Only students have a calendar.'}, status=400)

        today = timezone.localdate()
        try:
            month = int(request.query_params.get('month', today.month))
            year  = int(request.query_params.get('year',  today.year))
        except ValueError:
            return Response({'detail': 'Invalid month or year.'}, status=400)

        days, stats = _build_calendar_data(student, year, month)
        return Response({
            'month':        date(year, month, 1).strftime('%B %Y'),
            'year':         year,
            'month_number': month,
            'days':         days,
            'stats':        stats,
        })


# ══════════════════════════════════════════════════════════════════════════════
# Attendance Report
# ══════════════════════════════════════════════════════════════════════════════

class AttendanceReportView(APIView):
    """
    GET /api/mobile/attendance/report/?month=4&year=2026
    Calendar + stats + performance trend line data.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        student = _get_student(request.user)
        if not student:
            return Response({'detail': 'Only students have an attendance report.'}, status=400)

        today = timezone.localdate()
        try:
            month = int(request.query_params.get('month', today.month))
            year  = int(request.query_params.get('year',  today.year))
        except ValueError:
            return Response({'detail': 'Invalid month or year.'}, status=400)

        days, stats = _build_calendar_data(student, year, month)

        # Build cumulative performance trend
        trend = []
        present_so_far = 0
        total_so_far   = 0
        for d in days:
            if d['status'] in ('PRESENT', 'LATE', 'ABSENT'):
                total_so_far += 1
                if d['status'] in ('PRESENT', 'LATE'):
                    present_so_far += 1
            rate = round((present_so_far / total_so_far * 100), 1) if total_so_far else 0.0
            trend.append({
                'date':         d['date'],
                'date_display': date.fromisoformat(d['date']).strftime('%d %b'),
                'rate':         rate,
            })

        return Response({
            'month':             date(year, month, 1).strftime('%B %Y'),
            'year':              year,
            'month_number':      month,
            'days':              days,
            'stats':             stats,
            'performance_trend': trend,
        })


# ══════════════════════════════════════════════════════════════════════════════
# Attendance History (paginated list)
# ══════════════════════════════════════════════════════════════════════════════

class MobileAttendanceHistoryView(generics.ListAPIView):
    """
    GET /api/mobile/attendance/history/
    ?month=5&year=2026&status=PRESENT
    """
    from attendance.serializers import AttendanceLogSerializer as _S
    serializer_class   = _S
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student = _get_student(self.request.user)
        if not student:
            return AttendanceLog.objects.none()
        qs = AttendanceLog.objects.filter(student=student).order_by('-timestamp')
        month = self.request.query_params.get('month')
        year  = self.request.query_params.get('year')
        if month and year:
            try:
                qs = qs.filter(date__month=int(month), date__year=int(year))
            except ValueError:
                pass
        sf = self.request.query_params.get('status')
        if sf:
            qs = qs.filter(status=sf.upper())
        return qs


# ══════════════════════════════════════════════════════════════════════════════
# Analytics
# ══════════════════════════════════════════════════════════════════════════════

class AnalyticsView(APIView):
    """
    GET /api/mobile/analytics/?months=5
    Returns attendance %, punctuality %, current-month distribution,
    and monthly trends bar chart data.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        student = _get_student(request.user)
        if not student:
            return Response({'detail': 'Only students have analytics.'}, status=400)

        today = timezone.localdate()
        num_months = min(int(request.query_params.get('months', 5)), 12)

        # ── overall attendance & punctuality (all time) ──
        all_logs = AttendanceLog.objects.filter(student=student)
        total    = all_logs.count()
        present  = all_logs.filter(status='PRESENT').count()
        late     = all_logs.filter(status='LATE').count()
        att_pct  = round(((present + late) / total * 100), 1) if total else 0.0
        punc_pct = round((present / (present + late) * 100), 1) if (present + late) else 0.0

        # ── current month distribution ──
        _, days_in_month = monthrange(today.year, today.month)
        curr_logs = all_logs.filter(date__year=today.year, date__month=today.month)
        curr_leaves = LeaveRequest.objects.filter(
            student=student,
            status__in=['PENDING', 'APPROVED'],
            start_date__lte=today.replace(day=days_in_month),
            end_date__gte=today.replace(day=1),
        )
        leave_days = 0
        m_start = today.replace(day=1)
        m_end   = today.replace(day=days_in_month)
        for lr in curr_leaves:
            d = max(lr.start_date, m_start)
            while d <= min(lr.end_date, m_end):
                leave_days += 1
                d += timedelta(days=1)

        c_present = curr_logs.filter(status='PRESENT').count()
        c_late    = curr_logs.filter(status='LATE').count()
        c_absent  = days_in_month - c_present - c_late - leave_days

        distribution = {
            'month':      today.strftime('%B %Y'),
            'total_days': days_in_month,
            'present':    c_present,
            'absent':     max(c_absent, 0),
            'late':       c_late,
            'leave':      leave_days,
        }

        # ── monthly trends (last N months) ──
        trends = []
        for i in range(num_months - 1, -1, -1):
            ref = (today.replace(day=1) - timedelta(days=i * 28)).replace(day=1)
            m_logs = all_logs.filter(date__year=ref.year, date__month=ref.month)
            _, dim = monthrange(ref.year, ref.month)
            mp = m_logs.filter(status='PRESENT').count()
            ml = m_logs.filter(status='LATE').count()
            ma = m_logs.filter(status='ABSENT').count()
            trends.append({
                'month': ref.strftime('%b'), 'month_number': ref.month,
                'year': ref.year, 'present': mp, 'late': ml,
                'absent': ma, 'total': dim,
            })

        return Response({
            'attendance_percentage':  att_pct,
            'punctuality_percentage': punc_pct,
            'distribution':           distribution,
            'monthly_trends':         trends,
        })


# ══════════════════════════════════════════════════════════════════════════════
# Export (CSV / PDF)
# ══════════════════════════════════════════════════════════════════════════════

class ExportCSVView(APIView):
    """
    GET /api/mobile/export/csv/?month=5&year=2026
    Downloads a CSV file of the student's attendance for the given month.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        student = _get_student(request.user)
        if not student:
            return Response({'detail': 'Only students can export data.'}, status=400)

        today = timezone.localdate()
        try:
            month = int(request.query_params.get('month', today.month))
            year  = int(request.query_params.get('year',  today.year))
        except ValueError:
            return Response({'detail': 'Invalid month or year.'}, status=400)

        days, stats = _build_calendar_data(student, year, month)

        filename = f"attendance_{student.user.full_name.replace(' ','_')}_{year}_{month:02d}.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Day', 'Status', 'Check-In Time', 'Leave'])
        for d in days:
            writer.writerow([
                d['date'], d['weekday'], d['status'],
                d['time_in'] or '--', 'Yes' if d['is_leave'] else 'No',
            ])
        writer.writerow([])
        writer.writerow(['Summary'])
        writer.writerow(['Attendance Rate', stats['attendance_rate']])
        writer.writerow(['Avg Check-In',    stats['avg_check_in'] or '--'])
        writer.writerow(['Days Absent',     stats['days_absent']])
        writer.writerow(['Leave Days',      stats['leave_days']])
        return response


class ExportPDFView(APIView):
    """
    GET /api/mobile/export/pdf/?month=5&year=2026
    Downloads a PDF attendance report. Requires reportlab.
    Falls back to plain-text if reportlab is not installed.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        student = _get_student(request.user)
        if not student:
            return Response({'detail': 'Only students can export data.'}, status=400)

        today = timezone.localdate()
        try:
            month = int(request.query_params.get('month', today.month))
            year  = int(request.query_params.get('year',  today.year))
        except ValueError:
            return Response({'detail': 'Invalid month or year.'}, status=400)

        days, stats = _build_calendar_data(student, year, month)
        month_label = date(year, month, 1).strftime('%B %Y')

        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet
            import io

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4)
            styles = getSampleStyleSheet()
            elems = []

            elems.append(Paragraph(f'Attendance Report — {month_label}', styles['Title']))
            elems.append(Paragraph(f'Name: {student.user.full_name}', styles['Normal']))
            elems.append(Spacer(1, 12))

            data = [['Date', 'Day', 'Status', 'Check-In', 'Leave']]
            for d in days:
                data.append([
                    d['date'], d['weekday'], d['status'],
                    d['time_in'] or '--', 'Yes' if d['is_leave'] else 'No',
                ])
            data.append([])
            data.append(['Attendance Rate', stats['attendance_rate'], '', '', ''])
            data.append(['Avg Check-In',    stats['avg_check_in'] or '--', '', '', ''])
            data.append(['Days Absent',     str(stats['days_absent']), '', '', ''])
            data.append(['Leave Days',      str(stats['leave_days']), '', '', ''])

            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d6a4f')),
                ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
                ('GRID',       (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE',   (0, 0), (-1, -1), 9),
            ]))
            elems.append(t)
            doc.build(elems)

            buf.seek(0)
            filename = f"attendance_{student.user.full_name.replace(' ','_')}_{year}_{month:02d}.pdf"
            resp = HttpResponse(buf, content_type='application/pdf')
            resp['Content-Disposition'] = f'attachment; filename="{filename}"'
            return resp

        except ImportError:
            return Response({
                'detail': 'PDF export requires reportlab. Install with: pip install reportlab',
                'fallback': f'/api/mobile/export/csv/?month={month}&year={year}',
            }, status=501)


# ══════════════════════════════════════════════════════════════════════════════
# Notifications
# ══════════════════════════════════════════════════════════════════════════════

class MobileNotificationsView(generics.ListAPIView):
    """
    GET /api/mobile/notifications/
    ?filter=all|unread|attendance|system   (default: all)
    ?page=1
    """
    serializer_class   = MobileNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student = _get_student(self.request.user)
        if not student:
            return Notification.objects.none()

        qs = Notification.objects.filter(student=student).order_by('-created_at')
        f  = self.request.query_params.get('filter', 'all').lower()

        if f == 'unread':
            qs = qs.exclude(status=Notification.STATUS_SENT)
        elif f == 'attendance':
            qs = qs.filter(notification_type='ATTENDANCE')
        elif f == 'system':
            qs = qs.filter(notification_type__in=['ALERT', 'SYSTEM'])
        return qs


class MobileUnreadCountView(APIView):
    """GET /api/mobile/notifications/unread-count/"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        student = _get_student(request.user)
        if not student:
            return Response({'unread_count': 0})
        count = Notification.objects.filter(
            student=student
        ).exclude(status=Notification.STATUS_SENT).count()
        return Response({'unread_count': count})


class MobileMarkReadView(APIView):
    """POST /api/mobile/notifications/mark-read/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        student = _get_student(request.user)
        if not student:
            return Response({'detail': 'Only students have notifications.'}, status=400)
        s = MarkNotificationsReadSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        ids = s.validated_data.get('notification_ids', [])
        qs  = Notification.objects.filter(student=student).exclude(status=Notification.STATUS_SENT)
        if ids:
            qs = qs.filter(id__in=ids)
        count = qs.update(status=Notification.STATUS_SENT, sent_at=timezone.now())
        return Response({'marked': count})


# ══════════════════════════════════════════════════════════════════════════════
# Leave Requests (educational orgs only)
# ══════════════════════════════════════════════════════════════════════════════

class MobileLeaveRequestListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/mobile/leave-requests/
    POST /api/mobile/leave-requests/
    reason choices: VACATION | SICK | PERSONAL
    """
    permission_classes = [permissions.IsAuthenticated, IsEducationalOrg]
    parser_classes     = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        return MobileLeaveRequestCreateSerializer if self.request.method == 'POST' else MobileLeaveRequestSerializer

    def get_queryset(self):
        student = _get_student(self.request.user)
        return LeaveRequest.objects.filter(student=student).order_by('-created_at') if student else LeaveRequest.objects.none()

    def perform_create(self, serializer):
        student = _get_student(self.request.user)
        if not student:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only student accounts can submit leave requests.')
        serializer.save(student=student)

    def create(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        self.perform_create(s)
        return Response(
            MobileLeaveRequestSerializer(s.instance, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class MobileLeaveRequestDetailView(generics.RetrieveDestroyAPIView):
    """
    GET    /api/mobile/leave-requests/<uuid>/
    DELETE /api/mobile/leave-requests/<uuid>/  — withdraw (PENDING only)
    """
    serializer_class   = MobileLeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsEducationalOrg]

    def get_queryset(self):
        student = _get_student(self.request.user)
        return LeaveRequest.objects.filter(student=student) if student else LeaveRequest.objects.none()

    def destroy(self, request, *args, **kwargs):
        leave = self.get_object()
        if leave.status != LeaveRequest.STATUS_PENDING:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Only pending requests can be withdrawn.')
        return super().destroy(request, *args, **kwargs)
