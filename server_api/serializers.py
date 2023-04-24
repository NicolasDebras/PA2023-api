from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Friend, Participant, Party

class FriendSerializers(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'


class PlayerSerializers(serializers.ModelSerializer):
    friend = FriendSerializers(many=True, allow_null=True, read_only=True)

    class Meta:
        User = get_user_model()
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'commentaire', 'friend')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(**validated_data)
        return user


class ParticipantSerializers(serializers.ModelSerializer): 
    player = PlayerSerializers(allow_null=True, read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'accepting', 'player']


class PartySerializers(serializers.ModelSerializer): 
    participant_party = ParticipantSerializers(many= True, allow_null=True, read_only=True)
    Founder = PlayerSerializers(read_only=True)

    class Meta:
        model = Party
        fields = ['id', 'title', 'Founder', 'url_image', 'started', 'created_at','participant_party']



    