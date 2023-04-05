from .serializers import PlayerSerializers
from .models import Player
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework import viewsets

# Create your views here.
class PlayerViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = PlayerSerializers