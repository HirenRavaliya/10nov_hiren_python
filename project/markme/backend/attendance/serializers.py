from rest_framework import serializers
from .models import AttendanceLog, Notification, LeaveRequest
from accounts.serializers import StudentSerializer


class AttendanceLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    student_id = serializers.UUIDField(source='student.id', read_only=True)
    profile_photo = serializers.SerializerMethodField()
    date_display = serializers.DateField(source='date', read_only=True, format='%d %b %Y')
    time_display = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceLog
        fields = [
            'id', 'student_id', 'student_name', 'profile_photo',
            'timestamp', 'date', 'date_display', 'time_display',
            'status', 'method', 'confidence', 'notes',
        ]
        read_only_fields = ['id', 'timestamp', 'date']

    def get_profile_photo(self, obj):
        request = self.context.get('request')
        if obj.student.profile_photo and hasattr(obj.student.profile_photo, 'url'):
            url = obj.student.profile_photo.url
            if request:
                return request.build_absolute_uri(url)
            return url
        return None

    def get_time_display(self, obj):
        return obj.timestamp.strftime('%I:%M %p')


class ManualAttendanceSerializer(serializers.Serializer):
    """Mark attendance manually for a student."""
    student_id = serializers.UUIDField()
    status = serializers.ChoiceField(choices=AttendanceLog.STATUS_CHOICES, default='PRESENT')
    notes = serializers.CharField(required=False, allow_blank=True)


class FaceScanSerializer(serializers.Serializer):
    """Face scan from webcam – accepts base64 image or file upload."""
    image = serializers.ImageField(required=False)
    image_base64 = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get('image') and not data.get('image_base64'):
            raise serializers.ValidationError('Provide either `image` (file) or `image_base64`.')
        return data


class NotificationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'student_id', 'student_name', 'notification_type',
            'title', 'message', 'status', 'sent_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'sent_at']


class AttendanceSummarySerializer(serializers.Serializer):
    """Daily summary stats for the dashboard."""
    date = serializers.DateField()
    total_students = serializers.IntegerField()
    present_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()
    attendance_rate = serializers.FloatField()


class LeaveRequestSerializer(serializers.ModelSerializer):
    """Full detail — used by admin/teacher list views."""
    student_name    = serializers.CharField(source='student.user.full_name', read_only=True)
    student_email   = serializers.CharField(source='student.user.email', read_only=True)
    student_id      = serializers.UUIDField(source='student.id', read_only=True)
    reviewed_by_name = serializers.SerializerMethodField()
    duration_days   = serializers.IntegerField(read_only=True)
    proof_doc_url   = serializers.SerializerMethodField()
    reason_display  = serializers.CharField(source='get_reason_display', read_only=True)
    status_display  = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = LeaveRequest
        fields = [
            'id', 'student_id', 'student_name', 'student_email',
            'reason', 'reason_display', 'description',
            'start_date', 'end_date', 'duration_days',
            'proof_doc', 'proof_doc_url',
            'status', 'status_display',
            'reviewed_by_name', 'review_note', 'reviewed_at',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'status', 'reviewed_by_name', 'reviewed_at', 'created_at', 'updated_at']

    def get_reviewed_by_name(self, obj):
        return obj.reviewed_by.full_name if obj.reviewed_by else None

    def get_proof_doc_url(self, obj):
        request = self.context.get('request')
        if obj.proof_doc:
            url = obj.proof_doc.url
            return request.build_absolute_uri(url) if request else url
        return None


class LeaveRequestCreateSerializer(serializers.ModelSerializer):
    """Used by students/parents (mobile app) to submit a leave request."""
    class Meta:
        model  = LeaveRequest
        fields = ['reason', 'description', 'start_date', 'end_date', 'proof_doc']

    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError({'end_date': 'End date must be on or after start date.'})
        return data


class LeaveRequestReviewSerializer(serializers.Serializer):
    """Used by admin/teacher to approve or reject."""
    action      = serializers.ChoiceField(choices=['approve', 'reject'])
    review_note = serializers.CharField(required=False, allow_blank=True)
