from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/attendance/live/$', consumers.AttendanceConsumer.as_asgi()),
]
