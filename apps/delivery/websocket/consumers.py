import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DeliveryTrackingConsumer(AsyncWebsocketConsumer):
    """
    Consumer for customers to listen to live delivery boy GPS updates.
    """
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f"delivery_track_{self.order_id}"

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

    async def location_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'location_update',
            'data': message
        }))


class DeliveryBoyLocationConsumer(AsyncWebsocketConsumer):
    """
    Consumer for delivery boys to push their live GPS location to the server.
    """
    async def connect(self):
        self.delivery_boy_id = self.scope['url_route']['kwargs']['delivery_boy_id']
        self.group_name = f"delivery_boy_{self.delivery_boy_id}"

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

    async def receive(self, text_data):
        # Delivery boy sends their location here: {"order_id": "123", "lat": 28.1, "lng": 77.2}
        try:
            data = json.loads(text_data)
            order_id = data.get('order_id')
            lat = data.get('lat')
            lng = data.get('lng')

            if order_id and lat and lng:
                # Forward this location to the customer's tracking group
                track_group = f"delivery_track_{order_id}"
                await self.channel_layer.group_send(
                    track_group,
                    {
                        'type': 'location_update',
                        'message': {
                            'lat': lat,
                            'lng': lng
                        }
                    }
                )
        except json.JSONDecodeError:
            pass
