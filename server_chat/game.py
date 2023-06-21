import json
from pickle import FALSE
from . import sundox
from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['party_id']
        # Accepter la connexion WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Vous pouvez ajouter ici une logique à exécuter lors de la déconnexion, si nécessaire
        pass

    async def receive(self, text_data):
        # Charger les données reçues
        text_data_json = json.loads(text_data)
        # Réponse statique en JSON
        response = sundox.run_in_sandbox("./app/morpion.py", text_data_json)

        print(json.loads(response))
        
        # Envoyer la réponse directement au client
        await self.send(text_data=json.dumps(json.loads(response)))
