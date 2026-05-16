"""
WebSocket consumer for live scanner updates.
Broadcasts real-time attendance events to the admin dashboard.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class AttendanceConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = 'attendance_live'

    async def connect(self):
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'type': 'connected', 'message': 'Live attendance stream active.'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)

    async def receive(self, text_data):
        # Client can send a ping
        data = json.loads(text_data)
        if data.get('type') == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong'}))

    async def attendance_event(self, event):
        """Called when group_send broadcasts an attendance event."""
        await self.send(text_data=json.dumps(event['data']))
