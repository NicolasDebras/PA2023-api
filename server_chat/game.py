import json
from pickle import FALSE
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
        response = {
            "displays": [
            {
                  "width": "300",
                  "height": "300",
                  "content": [
                  {
                  "tag": "style",
                  "content": "line{stroke:black;stroke-width:4;}"
                  },
                  {
                  "tag": "line",
                  "x1": "0",
                  "y1": "100",
                  "x2": "300",
                  "y2": "100"
                  },
                  {
                  "tag": "line",
                  "x1": "100",
                  "y1": "0",
                  "x2": "100",
                  "y2": "300"
                  },
                  {
                  "tag": "line",
                  "x1": "0",
                  "y1": "200",
                  "x2": "300",
                  "y2": "200"
                  },
                  {
                  "tag": "line",
                  "x1": "200",
                  "y1": "0",
                  "x2": "200",
                  "y2": "300"
                  }
                  ],
                  "player": 1
            },
            {
                  "width": "300",
                  "height": "300",
                  "content": [
                  {
                  "tag": "style",
                  "content": "line{stroke:black;stroke-width:4;}"
                  },
                  {
                  "tag": "line",
                  "x1": "0",
                  "y1": "100",
                  "x2": "300",
                  "y2": "100"
                  },
                  {
                  "tag": "line",
                  "x1": "100",
                  "y1": "0",
                  "x2": "100",
                  "y2": "300"
                  },
                  {
                  "tag": "line",
                  "x1": "0",
                  "y1": "200",
                  "x2": "300",
                  "y2": "200"
                  },
                  {
                  "tag": "line",
                  "x1": "200",
                  "y1": "0",
                  "x2": "200",
                  "y2": "300"
                  }
                  ],
                  "player": 2
            }
            ],
            "requested_actions": [
            {
                  "type": "CLICK",
                  "player": 1,
                  "zones": [
                  {
                  "x": 0,
                  "y": 0,
                  "width": 100,
                  "height": 100
                  },
                  {
                  "x": 0,
                  "y": 100,
                  "width": 100,
                  "height": 100
                  },
                  {
                  "x": 0,
                  "y": 200,
                  "width": 100,
                  "height": 100
                  },
                  {
                  "x": 100,
                  "y": 0,
                  "width": 100,
                  "height": 100
                  },
                  {
                  "x": 100,
                  "y": 100,
                  "width": 100,
                  "height": 100
                  },
                  {
                  "x": 100,
                  "y": 200,
                  "width": 100,
                  "height": 100
                  },
                  {
                  "x": 200,
                  "y": 0,
                  "width": 100,
                  "height": 100
                  },
                  {
                  "x": 200,
                  "y": 100,
                  "width": 100,
                  "height": 100
                  },
                  {
                  "x": 200,
                  "y": 200,
                  "width": 100,
                  "height": 100
                  }
                  ]
            }
            ],
            "game_state": {
            "scores": [
                  0,
                  0
            ],
            "game_over": False
            }
      }
        
        # Envoyer la réponse directement au client
        await self.send(text_data=json.dumps(response))
