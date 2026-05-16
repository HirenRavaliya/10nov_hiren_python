from django.contrib import admin
from .models import AttendanceLog, Notification, LeaveRequest


@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'method', 'confidence', 'timestamp')
    list_filter = ('status', 'method', 'date')
    search_fields = ('student__user__full_name',)
    ordering = ('-timestamp',)
    date_hierarchy = 'date'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('student', 'notification_type', 'title', 'status', 'sent_at', 'created_at')
    list_filter = ('status', 'notification_type')
    search_fields = ('student__user__full_name', 'title')
    ordering = ('-created_at',)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'reason', 'start_date', 'end_date', 'duration_days', 'status', 'reviewed_by', 'created_at')
    list_filter = ('status', 'reason')
    search_fields = ('student__user__full_name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'reviewed_at')
    actions = ['approve_selected', 'reject_selected']

    def approve_selected(self, request, queryset):
        from django.utils import timezone
        queryset.filter(status='PENDING').update(
            status='APPROVED', reviewed_by=request.user,
            review_note='Bulk approved via admin.', reviewed_at=timezone.now()
        )
        self.message_user(request, 'Selected requests approved.')
    approve_selected.short_description = 'Approve selected leave requests'

    def reject_selected(self, request, queryset):
        from django.utils import timezone
        queryset.filter(status='PENDING').update(
            status='REJECTED', reviewed_by=request.user,
            review_note='Bulk rejected via admin.', reviewed_at=timezone.now()
        )
        self.message_user(request, 'Selected requests rejected.')
    reject_selected.short_description = 'Reject selected leave requests'
