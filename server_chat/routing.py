from django.urls import re_path
from . import consumers, game


websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<party_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'^ws/game/(?P<party_id>\d+)/$', game.GameConsumer.as_asgi()),
]
