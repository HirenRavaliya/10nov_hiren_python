"""
Attendance models:
- AttendanceLog: records each attendance event per student
- Notification: records push notification sends
"""
import uuid
from django.db import models
from accounts.models import Student


class AttendanceLog(models.Model):
    PRESENT = 'PRESENT'
    ABSENT = 'ABSENT'
    LATE = 'LATE'
    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        (LATE, 'Late'),
    ]

    METHOD_FACE = 'FACE'
    METHOD_MANUAL = 'MANUAL'
    METHOD_CHOICES = [
        (METHOD_FACE, 'AI Face Recognition'),
        (METHOD_MANUAL, 'Manual Override'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PRESENT)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default=METHOD_FACE)
    confidence = models.FloatField(null=True, blank=True, help_text='Face recognition confidence 0-1')
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'attendance_logs'
        ordering = ['-timestamp']
        # Prevent duplicate attendance for the same student on the same day
        unique_together = ('student', 'date')

    def __str__(self):
        return f'{self.student.name} – {self.date} – {self.status}'


class Notification(models.Model):
    TYPE_ATTENDANCE = 'ATTENDANCE'
    TYPE_ALERT = 'ALERT'
    TYPE_SYSTEM = 'SYSTEM'
    TYPE_CHOICES = [
        (TYPE_ATTENDANCE, 'Attendance'),
        (TYPE_ALERT, 'Alert'),
        (TYPE_SYSTEM, 'System'),
    ]

    STATUS_PENDING = 'PENDING'
    STATUS_SENT = 'SENT'
    STATUS_FAILED = 'FAILED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SENT, 'Sent'),
        (STATUS_FAILED, 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notifications')
    attendance_log = models.ForeignKey(AttendanceLog, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_ATTENDANCE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'Notif for {self.student.name} – {self.status}'


class LeaveRequest(models.Model):
    REASON_VACATION  = 'VACATION'
    REASON_SICK      = 'SICK'
    REASON_PERSONAL  = 'PERSONAL'
    REASON_CHOICES = [
        (REASON_VACATION, 'Vacation'),
        (REASON_SICK,     'Sick'),
        (REASON_PERSONAL, 'Personal'),
    ]

    STATUS_PENDING  = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (STATUS_PENDING,  'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student      = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='leave_requests')
    reason       = models.CharField(max_length=20, choices=REASON_CHOICES)
    description  = models.TextField(blank=True, help_text='Additional details from the student/parent')
    start_date   = models.DateField()
    end_date     = models.DateField()
    proof_doc    = models.FileField(
        upload_to='leave_proofs/',
        null=True, blank=True,
        help_text='Medical certificate, letter, or any supporting document'
    )
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reviewed_by  = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='reviewed_leaves'
    )
    review_note  = models.TextField(blank=True, help_text='Note from admin/teacher when approving or rejecting')
    reviewed_at  = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leave_requests'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student.name} – {self.reason} ({self.start_date} → {self.end_date}) – {self.status}'

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1
