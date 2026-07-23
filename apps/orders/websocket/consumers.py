import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderStatusConsumer(AsyncWebsocketConsumer):
    """
    Consumer for customers to listen to their specific order updates.
    """
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f"order_{self.order_id}"

        # Join order group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave order group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from room group
    async def order_update(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'order_status_update',
            'data': message
        }))


class AdminDashboardConsumer(AsyncWebsocketConsumer):
    """
    Consumer for admins to listen to live dashboard updates (new orders, etc).
    """
    async def connect(self):
        # In a real app, verify self.scope['user'].is_admin here
        self.group_name = "admin_dashboard"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def dashboard_update(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'dashboard_update',
            'data': message
        }))
