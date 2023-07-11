import json
from pickle import FALSE
from . import sundox
from channels.generic.websocket import AsyncWebsocketConsumer
from server_api.models import Party, Play
from asgiref.sync import sync_to_async

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['party_id']
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        all_data = []

        if "init" in text_data:
            await self.clear_play()
        else:
            print("recupere tous infoSend précedent")
            plays = await self.fetch_plays()
            for play in plays:
                all_data.append(play.infoSend)

        all_data.append(text_data)
        print(all_data)
        list_dict = [json.loads(i) for i in all_data]
        response = sundox.run_in_sandbox("./app/morpion.py", list_dict)
        print("docker passé")
        if not response:
            await self.send(text_data=json.dumps('{"errors":"erreur dans la gestion du docker"}'))
            return
        if not isinstance(response[-1], dict):
            await self.send(text_data=json.dumps('{"errors":"retour du docker pas un dictionnaire"}'))
            return
        response_data = response[-1]
        await self.send(text_data=json.dumps(response_data))
        if "errors" not in response_data:
            await self.save_play(text_data)

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

