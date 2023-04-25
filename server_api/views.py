from .serializers import PlayerSerializers, FriendSerializers, PartySerializers, ParticipantSerializers, FriendSerializers
from .permissions import IsCreationOrIsAuthenticated, IsViewOrIsAuthenticated
from .models import Friend, Player, Party, Participant


from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination


# Create your views here.

#-----------------CRUD authomatique---------------------------------------------------


class PlayerViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    #queryset permet de créer un CRUD 
    queryset = User.objects.all()
    serializer_class = PlayerSerializers

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsCreationOrIsAuthenticated,)


class PartyPagination(PageNumberPagination):
    page_size = 10  # Nombre de parties par page
    page_size_query_param = 'page_size'
    max_page_size = 100

class PartyViewSet(viewsets.ModelViewSet):
    
    #queryset permet de créer un CRUD 
    queryset = Party.objects.all()
    serializer_class = PartySerializers

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsViewOrIsAuthenticated,)
    pagination_class = PartyPagination



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


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
def accept_invitation(request, participant_id):
    try:
        participant = Participant.objects.get(id=participant_id)
    except Participant.DoesNotExist:
        return Response(status=404)

    participant.accepting = True
    participant.save()
    
    serializer = ParticipantSerializers(participant)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def add_friend(request, player1_id, player2_id):
    if player1_id == player2_id:
        return Response(status=409)
    try:
        player1 = Player.objects.get(id=player1_id)
        player2 = Player.objects.get(id=player2_id)
    except Player.DoesNotExist:
        return Response(status=404)

    # Vérifier si les deux joueurs sont déjà amis
    if Friend.objects.filter(Player1=player1, Player2=player2).exists() or Friend.objects.filter(Player1=player2, Player2=player1).exists():
        return Response(status=409)  

    friend = Friend.objects.create(Player1=player1, Player2=player2)
    friend.save()

    serializer = FriendSerializers(friend)
    return Response(serializer.data, status=201)  


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
def accept_friendship(request, friend_id):
    try:
        friend = Friend.objects.get(id=friend_id)
    except Friend.DoesNotExist:
        return Response(status=404)

    friend.accepting = True
    friend.save()

    serializer = FriendSerializers(friend)
    return Response(serializer.data)


