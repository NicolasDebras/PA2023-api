from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Ajoutez le client à un groupe de chat en fonction de l'ID de l'utilisateur
        await self.channel_layer.group_add(
            str(self.scope['user'].id),
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Supprimez le client du groupe de chat lorsqu'il se déconnecte
        await self.channel_layer.group_discard(
            str(self.scope['user'].id),
            self.channel_name
        )

    async def receive(self, text_data):
        # Traitez le message de chat reçu
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Envoyer le message de chat à tous les membres du groupe de chat
        await self.channel_layer.group_send(
            str(self.scope['user'].id),
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Envoyer un message de chat à la connexion WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
