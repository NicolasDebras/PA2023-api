import json
from . import sundox
from channels.generic.websocket import AsyncWebsocketConsumer
from server_api.models import Party, Play
from asgiref.sync import sync_to_async

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['party_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        plays = await self.fetch_plays()
        all_data = []
        for play in plays:
            all_data.append(play.infoSend)
        if all_data:
            list_dict = [json.loads(i) for i in all_data]
            response = sundox.run_in_sandbox("./app/morpion.py", list_dict)
            if not response:
                await self.group_send_message('{"errors":"erreur dans la gestion du docker"}')
                return
            if not isinstance(response[-1], dict):
                await self.group_send_message('{"errors":"retour du docker pas un dictionnaire"}')
                return
            response_data = response[-1]
            await self.group_send_message(response_data)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        all_data = []

        if "init" in text_data:
            await self.clear_play()
        else:
            plays = await self.fetch_plays()
            for play in plays:
                all_data.append(play.infoSend)

        all_data.append(text_data)
        list_dict = [json.loads(i) for i in all_data]
        response = sundox.run_in_sandbox("./app/morpion.py", list_dict)
        if not response:
            await self.group_send_message('{"errors":"erreur dans la gestion du docker"}')
            return
        if not isinstance(response[-1], dict):
            await self.group_send_message('{"errors":"retour du docker pas un dictionnaire"}')
            return
        response_data = response[-1]
        if "errors" not in response_data:
            await self.group_send_message(response_data)
            await self.save_play(text_data)
        else:
           await self.send(response_data) 

    async def save_play(self, info_send):
        party_id = int(self.room_name)

        party = await sync_to_async(Party.objects.get)(id=party_id)

        play = Play(infoSend=info_send, party=party)
        await sync_to_async(play.save)()

    async def fetch_plays(self):
        party_id = int(self.room_name)
        party = await sync_to_async(Party.objects.get)(id=party_id)
        plays = await sync_to_async(list)(Play.objects.filter(party=party))
        return plays

    async def clear_play(self):
        party_id = int(self.room_name)
        party = await sync_to_async(Party.objects.get)(id=party_id)
        plays = await sync_to_async(Play.objects.filter)(party=party)
        await sync_to_async(plays.delete)()

    async def group_send_message(self, message):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': message
            }
        )

    async def game_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
