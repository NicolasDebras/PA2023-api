from .serializers import PlayerSerializers, FriendSerializers, PartySerializers, ParticipantSerializers, FriendSerializers, MessageSerializers, FullPartySerializers
from .permissions import IsCreationOrIsAuthenticated, IsViewOrIsAuthenticated
from .models import Friend, Player, Party, Participant, Message


from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

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


class Pagination(PageNumberPagination):
    page_size = 9  # Nombre de parties par page
    page_size_query_param = 'page_size'
    max_page_size = 100

class PartyViewSet(viewsets.ModelViewSet):
    #queryset permet de créer un CRUD 
    queryset = Party.objects.all()
    serializer_class = PartySerializers

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsViewOrIsAuthenticated,)
    pagination_class = Pagination


class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializers

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsCreationOrIsAuthenticated,)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        token = response.data['token']
        user_id = Token.objects.get(key=token).user_id
        return Response({'token': token, 'user_id': user_id})

class MyPartyView(APIView):
    pagination_class = Pagination()

    def get(self, request, id_player):
        try:
            founded_parties = Party.objects.filter(Founder_id=id_player)
            participated_parties = Party.objects.filter(participant_party__player_id=id_player)

            # On pagine les résultats ici
            parties = founded_parties.union(participated_parties).order_by('id')
            parties_page = self.pagination_class.paginate_queryset(parties, request)

            serialized_parties = PartySerializers(parties_page, many=True).data
            return self.pagination_class.get_paginated_response(serialized_parties)

        except Party.DoesNotExist:
            raise Response(status=404, data={"Mauvais d'id" : id_player})
        except Exception as e:
            return Response(data={'error': str(e)}, status=500)
        

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
        return Response(status=201, data={"id": participant.id})  # Objet créé
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

    friend = Friend.objects.create(Player1=player1, Player2=player2, who_ask=player1)
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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def OneParty(request, party_id):
    try:
        party = Party.objects.get(id=party_id)
    except:
        return Response(status=404)

    serializer = FullPartySerializers(party)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_party(request, party_id):
    try:
        party = Party.objects.get(id=party_id)
    except Party.DoesNotExist:
        return Response({"error": "Party not found"}, status=404)

    serializer = PartySerializers(party, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=404)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def patybyuser(request, user_id):
    try:
        party = Party.objects.getAll(player=user_id)
    except:
        return Response(status=404)

    serializer = PartySerializers(party)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def MessageByUser(request, party_id):
    try:
        messages = list(Message.objects.filter(party_id=party_id).order_by('-timestamp')[:10])
        messages.reverse()
    except Message.DoesNotExist:
        return Response(status=404)

    serializer = MessageSerializers(messages, many=True)
    return Response(serializer.data)



    ## To do for reset

# User = get_user_model()
# class PasswordResetView(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = PasswordResetSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = User.objects.get(email=serializer.validated_data['email'])

#         # Crée un token de réinitialisation de mot de passe
#         token = user.password_reset_token()
#         user.save()

#         # Envoie l'email de réinitialisation de mot de passe à l'utilisateur
#         subject = 'Réinitialisation de votre mot de passe'
#         message = render_to_string('reset_password_email.html', {
#             'user': user,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': token,
#             'reset_url': reverse('password_reset_confirm'),
#         })
#         send_mail(subject, message, 'noreply@example.com', [user.email])

#         return Response({'detail': 'Un email de réinitialisation de mot de passe vous a été envoyé.'}, status=status.HTTP_200_OK)

# class PasswordResetConfirmView(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = PasswordResetConfirmSerializer

#     def get_user(self, uidb64):
#         try:
#             uid = urlsafe_base64_decode(uidb64).decode()
#             user = User.objects.get(pk=uid)
#             return user
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             return None

#     def get(self, request, uidb64):
