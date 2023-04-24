from .serializers import PlayerSerializers, FriendSerializers, PartySerializers, ParticipantSerializers
from .permissions import IsCreationOrIsAuthenticated, IsViewOrIsAuthenticated
from .models import Friend, Player, Party, Participant


from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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

class PartyViewSet(viewsets.ModelViewSet):
    
    #queryset permet de créer un CRUD 
    queryset = Party.objects.all()
    serializer_class = PartySerializers

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsViewOrIsAuthenticated,)


class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializers

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsCreationOrIsAuthenticated,)


#-----------------Requete classique---------------------------------------------------

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def PlayerFindWithUsername(request, username):
    try:
        player = Player.objects.get(username=username)
    except:
        return Response(status=404)
    serializers = PlayerSerializers(player)
    return Response(serializers.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def AddParticipant(request, player, party):
    try:
        pt = Party.objects.get(id=party)
        pl = Player.objects.get(id=player)
    except:
        return Response(status=404)
    # Utilisation de la méthode get_or_create pour éviter les doublons
    participant, created = Participant.objects.get_or_create(party=pt, player=pl)

    if created:
        participant.save()
        return Response(status=201)  # Objet créé
    else:
        return Response(status=409)  # Objet déjà existant
