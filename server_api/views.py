from .serializers import PlayerSerializers, FriendSerializers

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCreationOrIsAuthenticated
from .models import Friend, Player
from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.

#-----------------CRUD authomatique---------------------------------------------------


class PlayerViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    #queryset permet de créer un CRUD 
    queryset = User.objects.all()
    serializer_class = PlayerSerializers

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsCreationOrIsAuthenticated,)



class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializers

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsCreationOrIsAuthenticated,)


#-----------------Requete classique---------------------------------------------------

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsCreationOrIsAuthenticated])
def PlayerFindWithUsername(request, username):
    try:
        player = Player.objects.get(username=username)
    except:
        return Response(status=404)
    serializers = PlayerSerializers(player)
    return Response(serializers.data)