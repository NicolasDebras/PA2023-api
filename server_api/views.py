from .serializers import PlayerSerializers, FriendSerializers, PartySerializers, ParticipantSerializers, FriendSerializers,PasswordResetSerializer,PasswordResetConfirmSerializer
from .permissions import IsCreationOrIsAuthenticated, IsViewOrIsAuthenticated
from .models import Friend, Player, Party, Participant


from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
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
    page_size = 9  # Nombre de parties par page
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


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        token = response.data['token']
        user_id = Token.objects.get(key=token).user_id
        return Response({'token': token, 'user_id': user_id})



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
    return Response(status=200)

    ## To do for reset
class PasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request, player_id):
         serializer = self.serializer_class(data=request.data)
         serializer.is_valid(raise_exception=True)
         try:
            user = Player.objects.get(id=player_id)
         except:
                print(player_id)
                return Response(status=404)

         # Crée un token de réinitialisation de mot de passe
         token_generator = PasswordResetTokenGenerator()
         token = token_generator.make_token(user)
         user.save()
         uid64=urlsafe_base64_encode(force_bytes(user.pk))
#         # Envoie l'email de réinitialisation de mot de passe à l'utilisateur
         subject = 'Réinitialisation de votre mot de passe'
         current_site = get_current_site(request)
         message = render_to_string('registration/password_reset_email.html', {
             'user': user,
             'uid': uid64,
             'token': token,
             'domain':current_site,
             'reset_url': reverse('password_reset_confirm',args=(uid64, token)),
         })
         print([user.email])
         send_mail(subject, message, 'noreply@example.com', [user.email])

         return Response({'detail': 'Un email de réinitialisation de mot de passe vous a été envoyé.'}, status=200)

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def get_user(self,request, uidb64,token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            return user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None
 