"""
ASGI config for backend project.
Supports both HTTP (via Django) and WebSocket (via Django Channels).
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django_asgi_app = get_asgi_application()

from attendance import routing as attendance_routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            attendance_routing.websocket_urlpatterns
        )
    ),
})
