"""
Firebase Cloud Messaging (FCM) push notification helper.
Sends push notifications to students' mobile app when attendance is marked.
Falls back gracefully if Firebase credentials are not configured.
"""
import logging
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

_firebase_initialized = False


def _init_firebase():
    global _firebase_initialized
    if _firebase_initialized:
        return True
    cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', '')
    if not cred_path:
        logger.info('Firebase credentials not configured. Push notifications disabled.')
        return False
    try:
        import firebase_admin
        from firebase_admin import credentials
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        return True
    except Exception as e:
        logger.warning(f'Firebase init failed: {e}')
        return False


def send_push_notification(fcm_token: str, title: str, body: str, data: dict = None):
    """
    Send a push notification to a single device.
    Returns True on success, False otherwise.
    """
    if not _init_firebase():
        logger.info(f'[PUSH SKIPPED – no Firebase] Title: {title} | Body: {body}')
        return False

    try:
        from firebase_admin import messaging
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data={k: str(v) for k, v in (data or {}).items()},
            token=fcm_token,
        )
        response = messaging.send(message)
        logger.info(f'Push sent: {response}')
        return True
    except Exception as e:
        logger.error(f'Push notification failed: {e}')
        return False


def notify_attendance_marked(student, attendance_log):
    """
    Send attendance confirmation notification to the student's mobile app.
    Also creates/updates a Notification DB record.
    """
    from attendance.models import Notification

    title = '✅ Attendance Marked!'
    body = (
        f'Hi {student.user.full_name}, your attendance has been successfully '
        f'recorded at {attendance_log.timestamp.strftime("%I:%M %p")} '
        f'on {attendance_log.date.strftime("%d %b %Y")}.'
    )

    notif = Notification.objects.create(
        student=student,
        attendance_log=attendance_log,
        notification_type=Notification.TYPE_ATTENDANCE,
        title=title,
        message=body,
        status=Notification.STATUS_PENDING,
    )

    # Try to send push if student has FCM token
    fcm_token = student.user.fcm_token
    if fcm_token:
        success = send_push_notification(
            fcm_token=fcm_token,
            title=title,
            body=body,
            data={
                'type': 'attendance',
                'attendance_id': str(attendance_log.id),
                'student_id': str(student.id),
                'date': str(attendance_log.date),
            }
        )
        if success:
            notif.status = Notification.STATUS_SENT
            notif.sent_at = timezone.now()
        else:
            notif.status = Notification.STATUS_FAILED
    else:
        notif.status = Notification.STATUS_FAILED
        logger.info(f'No FCM token for student {student.id} – notification saved to DB only.')

    notif.save()
    return notif
