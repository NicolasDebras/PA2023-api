import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from server_api.models import Message, Party, Player

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['party_id']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender_id = text_data_json['sender_id']
        message = text_data_json['message']
        await self.save_message(sender_id, message)
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        await self.send(text_data=json.dumps({'message': message, 'sender_id': sender_id}))

    @sync_to_async
    def save_message(self, sender_id, message):
        sender = Player.objects.get(id=sender_id)
        party = Party.objects.get(id=self.room_name)
        Message.objects.create(sender=sender, content=message, party=party)
