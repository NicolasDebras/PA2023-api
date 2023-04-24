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
    User = get_user_model()
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
        pl = Player.objects.get(id=player)
        pt = Party.objects.get(id=party)
    except:
        return Response(status=404)
    participant = Participant.objects.create(party=pt, player=pl)
    participant.save()
    return Response(status=200)

    ## To do for reset

User = get_user_model()
class PasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data['email'])

        # Crée un token de réinitialisation de mot de passe
        token = user.password_reset_token()
        user.save()

        # Envoie l'email de réinitialisation de mot de passe à l'utilisateur
        subject = 'Réinitialisation de votre mot de passe'
        message = render_to_string('reset_password_email.html', {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
            'reset_url': reverse('password_reset_confirm'),
        })
        send_mail(subject, message, 'noreply@example.com', [user.email])

        return Response({'detail': 'Un email de réinitialisation de mot de passe vous a été envoyé.'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            return user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def get(self, request, uidb64):