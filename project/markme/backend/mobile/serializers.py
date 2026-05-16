"""
Mobile App Serializers
======================
Covers all data shapes needed by the Flutter / React-Native mobile client:
  - Auth        : login response, token refresh
  - Profile     : student card, FCM token update
  - Calendar    : per-day status + monthly stats
  - Attendance Report : calendar + stats + performance trend
  - Analytics   : attendance %, punctuality %, distribution, monthly trends
  - Notifications : list (All/Unread/Attendance/System), mark-read, unread count
  - Leave Requests : submit (Vacation/Sick/Personal), list, detail (educational only)
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import Student, Teacher, Organization
from attendance.models import AttendanceLog, Notification, LeaveRequest

User = get_user_model()


# ── Auth ───────────────────────────────────────────────────────────────────────

class MobileTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extends JWT login with extra fields the mobile app needs right away."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['full_name'] = user.full_name
        token['role']      = user.role
        token['email']     = user.email
        token['org_type']  = user.org_type
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user_id']   = str(user.id)
        data['full_name'] = user.full_name
        data['role']      = user.role
        data['email']     = user.email
        data['phone']     = user.phone
        data['org_type']  = user.org_type

        if user.role == User.STUDENT:
            try:
                sp = user.student_profile
                data['student_id']      = str(sp.id)
                data['face_registered'] = sp.face_registered
                data['roll_number']     = sp.roll_number
                data['organization_id'] = str(sp.organization_id) if sp.organization_id else None
                data['org_name']        = sp.organization.name if sp.organization else None
            except Student.DoesNotExist:
                pass

        if user.role in (User.ADMIN, User.TEACHER):
            try:
                tp = user.teacher_profile
                data['organization_id'] = str(tp.organization_id) if tp.organization_id else None
                data['org_name']        = tp.organization.name if tp.organization else None
            except Teacher.DoesNotExist:
                data['organization_id'] = None
                data['org_name']        = None

        return data


# ── Profile ────────────────────────────────────────────────────────────────────

class MobileProfileSerializer(serializers.ModelSerializer):
    profile_pic_url = serializers.SerializerMethodField()
    student_id      = serializers.SerializerMethodField()
    face_registered = serializers.SerializerMethodField()
    roll_number     = serializers.SerializerMethodField()
    guardian_name   = serializers.SerializerMethodField()
    guardian_phone  = serializers.SerializerMethodField()
    guardian_email  = serializers.SerializerMethodField()
    organization_id = serializers.SerializerMethodField()
    org_name        = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = [
            'id', 'email', 'full_name', 'role', 'org_type', 'phone',
            'profile_pic_url',
            'student_id', 'face_registered', 'roll_number',
            'guardian_name', 'guardian_phone', 'guardian_email',
            'organization_id', 'org_name',
            'date_joined',
        ]

    def _sp(self, obj):
        try:
            return obj.student_profile
        except Exception:
            return None

    def _tp(self, obj):
        try:
            return obj.teacher_profile
        except Exception:
            return None

    def get_profile_pic_url(self, obj):
        request = self.context.get('request')
        if obj.profile_pic and hasattr(obj.profile_pic, 'url'):
            return request.build_absolute_uri(obj.profile_pic.url) if request else obj.profile_pic.url
        return None

    def get_student_id(self, obj):
        sp = self._sp(obj); return str(sp.id) if sp else None

    def get_face_registered(self, obj):
        sp = self._sp(obj); return sp.face_registered if sp else None

    def get_roll_number(self, obj):
        sp = self._sp(obj); return sp.roll_number if sp else None

    def get_guardian_name(self, obj):
        sp = self._sp(obj); return sp.guardian_name if sp else None

    def get_guardian_phone(self, obj):
        sp = self._sp(obj); return sp.guardian_phone if sp else None

    def get_guardian_email(self, obj):
        sp = self._sp(obj); return sp.guardian_email if sp else None

    def get_organization_id(self, obj):
        sp = self._sp(obj)
        if sp and sp.organization_id:
            return str(sp.organization_id)
        tp = self._tp(obj)
        if tp and tp.organization_id:
            return str(tp.organization_id)
        return None

    def get_org_name(self, obj):
        sp = self._sp(obj)
        if sp and sp.organization:
            return sp.organization.name
        tp = self._tp(obj)
        if tp and tp.organization:
            return tp.organization.name
        return None


class FCMTokenUpdateSerializer(serializers.Serializer):
    fcm_token = serializers.CharField()


# ── Calendar ───────────────────────────────────────────────────────────────────

class CalendarDaySerializer(serializers.Serializer):
    """One cell in the calendar grid."""
    date         = serializers.DateField()
    day          = serializers.IntegerField()
    weekday      = serializers.CharField()        # 'Mon', 'Tue' …
    status       = serializers.CharField()        # PRESENT | ABSENT | LEAVE | NONE
    time_in      = serializers.CharField(allow_null=True)   # '09:10 AM' or null
    is_leave     = serializers.BooleanField()
    is_today     = serializers.BooleanField()


class CalendarStatsSerializer(serializers.Serializer):
    """Four stat cards shown below the calendar."""
    attendance_rate = serializers.CharField()   # e.g. '71.4%'
    avg_check_in    = serializers.CharField(allow_null=True)   # e.g. '09:15 AM'
    days_absent     = serializers.IntegerField()
    leave_days      = serializers.IntegerField()


class CalendarResponseSerializer(serializers.Serializer):
    month        = serializers.CharField()      # 'April 2026'
    year         = serializers.IntegerField()
    month_number = serializers.IntegerField()
    days         = CalendarDaySerializer(many=True)
    stats        = CalendarStatsSerializer()


# ── Attendance Report ─────────────────────────────────────────────────────────

class PerformanceTrendPointSerializer(serializers.Serializer):
    """One point on the performance trend line chart."""
    date         = serializers.DateField()
    date_display = serializers.CharField()   # '01 May'
    rate         = serializers.FloatField()  # cumulative attendance rate up to this day


class AttendanceReportSerializer(serializers.Serializer):
    """Full attendance report: calendar + stats + performance trend."""
    month            = serializers.CharField()
    year             = serializers.IntegerField()
    month_number     = serializers.IntegerField()
    days             = CalendarDaySerializer(many=True)
    stats            = CalendarStatsSerializer()
    performance_trend = PerformanceTrendPointSerializer(many=True)


# ── Analytics ─────────────────────────────────────────────────────────────────

class MonthlyTrendItemSerializer(serializers.Serializer):
    """One bar group in the Monthly Trends bar chart."""
    month        = serializers.CharField()    # 'Jan', 'Feb' …
    month_number = serializers.IntegerField()
    year         = serializers.IntegerField()
    present      = serializers.IntegerField()
    late         = serializers.IntegerField()
    absent       = serializers.IntegerField()
    total        = serializers.IntegerField()


class DistributionSerializer(serializers.Serializer):
    """Current-month donut chart data."""
    month       = serializers.CharField()    # 'May 2026'
    total_days  = serializers.IntegerField()
    present     = serializers.IntegerField()
    absent      = serializers.IntegerField()
    late        = serializers.IntegerField()
    leave       = serializers.IntegerField()


class AnalyticsSerializer(serializers.Serializer):
    """Top-level analytics response."""
    attendance_percentage  = serializers.FloatField()   # overall % (present+late / total)
    punctuality_percentage = serializers.FloatField()   # % of present days that were on time (not LATE)
    distribution           = DistributionSerializer()
    monthly_trends         = MonthlyTrendItemSerializer(many=True)


# ── Notifications ──────────────────────────────────────────────────────────────

class MobileNotificationSerializer(serializers.ModelSerializer):
    time_ago = serializers.SerializerMethodField()
    is_read  = serializers.SerializerMethodField()
    type_label = serializers.SerializerMethodField()

    class Meta:
        model  = Notification
        fields = [
            'id', 'notification_type', 'type_label',
            'title', 'message', 'status',
            'sent_at', 'created_at', 'time_ago', 'is_read',
        ]

    def get_time_ago(self, obj):
        now   = timezone.now()
        delta = now - obj.created_at
        if delta.days >= 1:
            return f'{delta.days}d ago'
        hours = delta.seconds // 3600
        if hours >= 1:
            return f'{hours}h ago'
        mins = delta.seconds // 60
        return f'{mins}m ago' if mins > 0 else 'just now'

    def get_is_read(self, obj):
        return obj.status == Notification.STATUS_SENT

    def get_type_label(self, obj):
        return {
            'ATTENDANCE': 'Attendance',
            'ALERT':      'System',
            'SYSTEM':     'System',
        }.get(obj.notification_type, obj.notification_type.title())


class MarkNotificationsReadSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        help_text='Omit or pass empty list to mark ALL as read.'
    )


# ── Leave Requests ─────────────────────────────────────────────────────────────

class MobileLeaveRequestSerializer(serializers.ModelSerializer):
    """Full leave request — returned for list & retrieve."""
    duration_days    = serializers.IntegerField(read_only=True)
    reason_display   = serializers.CharField(source='get_reason_display', read_only=True)
    status_display   = serializers.CharField(source='get_status_display', read_only=True)
    proof_doc_url    = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    created_display  = serializers.SerializerMethodField()

    class Meta:
        model  = LeaveRequest
        fields = [
            'id', 'reason', 'reason_display', 'description',
            'start_date', 'end_date', 'duration_days',
            'proof_doc_url',
            'status', 'status_display',
            'reviewed_by_name', 'review_note', 'reviewed_at',
            'created_at', 'created_display',
        ]
        read_only_fields = ['id', 'status', 'reviewed_by_name', 'reviewed_at', 'created_at']

    def get_proof_doc_url(self, obj):
        request = self.context.get('request')
        if obj.proof_doc:
            url = obj.proof_doc.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_reviewed_by_name(self, obj):
        return obj.reviewed_by.full_name if obj.reviewed_by else None

    def get_created_display(self, obj):
        return obj.created_at.strftime('%d %b %Y')


class MobileLeaveRequestCreateSerializer(serializers.ModelSerializer):
    """Student submits a new leave request. Reason choices: VACATION, SICK, PERSONAL."""

    class Meta:
        model  = LeaveRequest
        fields = ['reason', 'description', 'start_date', 'end_date', 'proof_doc']

    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError({'end_date': 'End date must be on or after start date.'})
        return data
