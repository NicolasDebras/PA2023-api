from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Friend, Participant, Party
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from rest_framework import serializers
from .models import Friend, Participant, Party, Player, Message, ArgumentParty
from django.db.models import Q

class FriendSerializers(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'

class ArgumentPartySerializers(serializers.ModelSerializer):
    class Meta:
        model = ArgumentParty
        fields = ['id', 'name', 'value', 'type']

class LessPlayerSerializers(serializers.ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ('id', 'username', 'url_image')


class PlayerSerializers(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()
    invit = serializers.SerializerMethodField()

    class Meta:
        User = get_user_model()
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'commentaire', 'url_image' ,'friends', 'invit')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(**validated_data)
        return user

    def get_friends(self, obj):
        friends = Friend.objects.filter(Q(Player1=obj) | Q(Player2=obj), accepting=True)
        friend_data = []
        for friend in friends:
            if friend.Player1 == obj:
                friend_username = friend.Player2.username
                id = friend.id
                player_id = friend.Player2.id
                url_image = friend.Player2.url_image
            else:
                friend_username = friend.Player1.username
                id = friend.id
                player_id = friend.Player1.id
                url_image = friend.Player1.url_image
            friend_data.append({'username': friend_username,
                                'player_id': player_id,
                                'asc_id': id,
                                'url_image': url_image,})
        return friend_data
    
    def get_invit(self, obj):
        friends = Friend.objects.filter(Q(Player1=obj) | Q(Player2=obj), accepting=False)
        friend_data = []
        for friend in friends:
            id = friend.id
            who_ask = friend.who_ask
            if friend.Player1 == obj:
                friend_username = friend.Player2.username                
                player_id = friend.Player2.id
                other = friend.Player1.id
                url_image = friend.Player2.url_image
            else:
                friend_username = friend.Player1.username
                player_id = friend.Player1.id
                other = friend.Player2.id
                url_image = friend.Player1.url_image
            if who_ask.id != other:
                friend_data.append({'username': friend_username,
                                'player_id': player_id,
                                'asc_id': id,
                                'url_image': url_image,})
        return friend_data


class ParticipantSerializers(serializers.ModelSerializer): 
    player = LessPlayerSerializers(allow_null=True, read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'accepting', 'player']

class AcceptParticipantSerializers(serializers.ModelSerializer): 
    player = LessPlayerSerializers(allow_null=True, read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'player', 'tag_player', 'point']


class PartySerializers(serializers.ModelSerializer):
    accepting_participants = serializers.SerializerMethodField()
    pending_participants = serializers.SerializerMethodField()
    Founder = LessPlayerSerializers(read_only=True)
    founder_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(),
        source='Founder',
        write_only=True
    )

    class Meta:
        model = Party
        fields = ['id', 'title', 'Founder', 'url_image', 'started', 'created_at', 'accepting_participants', 'pending_participants', 'founder_id']
        read_only_fields = ['Founder']

    def get_accepting_participants(self, obj):
        accepting_participants = Participant.objects.filter(party=obj, accepting=True)
        return AcceptParticipantSerializers(accepting_participants, many=True).data

    def get_pending_participants(self, obj):
        pending_participants = Participant.objects.filter(party=obj, accepting=False)
        return ParticipantSerializers(pending_participants, many=True).data

    def create(self, validated_data):
        party = Party.objects.create(**validated_data)
        founder = Player.objects.filter(username=validated_data["Founder"]).first()
        Participant.objects.create(party=party, player=founder, accepting=True)
        

        return party

class FullPartySerializers(serializers.ModelSerializer):
    accepting_participants = serializers.SerializerMethodField()
    pending_participants = serializers.SerializerMethodField()
    fk_game_argument = ArgumentPartySerializers(many=True)
    Founder = LessPlayerSerializers(read_only=True)
    founder_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(),
        source='Founder',
        write_only=True
    )
    class Meta:
        model = Party
        fields = ['id', 'title', 'Founder', 'url_image', 'started', 'created_at', 'accepting_participants', 'pending_participants', 'founder_id', 'url_game', 'language', 'fk_game_argument', 'max_player']
        read_only_fields = ['Founder']

    def get_accepting_participants(self, obj):
        accepting_participants = Participant.objects.filter(party=obj, accepting=True)
        return AcceptParticipantSerializers(accepting_participants, many=True).data

    def get_pending_participants(self, obj):
        pending_participants = Participant.objects.filter(party=obj, accepting=False)
        return ParticipantSerializers(pending_participants, many=True).data
    
    

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'tag_player']

class PartyPatchSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)
    argument_parties = ArgumentPartySerializers(many=True, required=False)

    class Meta:
        model = Party
        fields = ['url_game', 'language', 'max_player', 'participants', 'argument_parties']


class MessageSerializers(serializers.ModelSerializer):
    sender = LessPlayerSerializers()  
    content = serializers.CharField(allow_blank=True)

    class Meta:
        model = Message
        fields = ('sender', 'content', 'timestamp')


## To do for reset

User = get_user_model()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if not user:
            raise serializers.ValidationError('Aucun utilisateur avec cet email n\'a été trouvé.')
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(write_only=True)

    def validate_token(self, value):
        user = self.context.get('user')
        if user is None or str(user.reset_password_token) != value:
            raise serializers.ValidationError('Le token de réinitialisation de mot de passe est invalide.')
        return value
     
    def save(self):
        user = self.context.get('user')
        password = self.validated_data['password']
        user.set_password(password)
        user.reset_password_token = None
        user.save()
        return user

    