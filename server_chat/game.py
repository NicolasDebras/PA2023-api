import json
import requests
from . import sundox
from channels.generic.websocket import AsyncWebsocketConsumer
from server_api.models import Party, Play
from asgiref.sync import sync_to_async
import os

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['party_id']
        self.room_group_name = 'game_%s' % self.room_name
        self.url_game = None

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        plays = await self.fetch_plays()
        self.url_game = await self.get_party_url_game()

        await self.download_game_file(self.url_game)

        print(self.url_game)

        all_data = []
        for play in plays:
            all_data.append(play.infoSend)
        if all_data:
            list_dict = [json.loads(i) for i in all_data]
            print("toto")
            response = await sync_to_async(sundox.run_in_sandbox)(os.path.abspath(self.url_game), list_dict)
            if not response:
                await self.group_send_message('{"errors":"erreur dans la gestion du docker"}')
                return
            if not isinstance(response[-1], dict):
                await self.group_send_message('{"errors":"retour du docker pas un dictionnaire"}')
                return
            response_data = response[-1]
            await self.group_send_message(response_data)

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        all_data = []
        print("toto")

        if "init" in text_data:
            await self.clear_play()
        else:
            plays = await self.fetch_plays()
            for play in plays:
                all_data.append(play.infoSend)
        if "delete" not in text_data:
            all_data.append(text_data)
        else: 
            if len(all_data) > 1:
                all_data.pop()
                await self.clear_last_play()
            else:
                self.send(text_data=json.dumps({"errors":"pas assez de donnée pour backs"}))
                return
        list_dict = [json.loads(i) for i in all_data]
        response = await sync_to_async(sundox.run_in_sandbox)(os.path.abspath(self.url_game), list_dict)
        if not response:
            await self.group_send_message('{"errors":"erreur dans la gestion du docker"}')
            return
        if not isinstance(response[-1], dict):
            await self.group_send_message('{"errors":"retour du docker pas un dictionnaire"}')
            return
        response_data = response[-1]
        if "errors" not in response_data:
            await self.group_send_message(response_data)
            if "delete" not in text_data:
                await self.save_play(text_data)
        else:
           await self.send(text_data=json.dumps(response_data))

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

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_message',
                'message': message
            }
        )

    async def game_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps(message))

    async def get_party_url_game(self):
        if self.url_game is None:
            party_id = int(self.room_name)
            party = await sync_to_async(Party.objects.get)(id=party_id)
            self.url_game = party.url_game

        return self.url_game
    
    
    async def download_game_file(self, url):
        local_filename = "./app/input" +self.room_group_name+ ".py"
        
        # requête HTTP pour télécharger le fichier
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)

        self.url_game = local_filename
    
    async def clear_last_play(self):
        party_id = int(self.room_name)
        party = await sync_to_async(Party.objects.get)(id=party_id)
        latest_play = await sync_to_async(Play.objects.filter(party=party).latest)('date_creation')
        if latest_play is not None:
            await sync_to_async(latest_play.delete)()
    
