from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Player(AbstractUser):
    pass
    url_image = models.CharField(max_length=500, null=True)
    commentaire = models.CharField(max_length=50).empty_strings_allowed

class Friend(models.Model): 
    Player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='friend1')
    Player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='friend2')
    who_ask = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='ask', null=True)

    #Si false -> juste une invitation 
    accepting = models.BooleanField(default=False)

class Party(models.Model): 
    title = models.CharField(max_length=50)
    Founder = models.ForeignKey(Player, related_name='founder', on_delete=models.CASCADE)
    url_image = models.CharField(max_length=500, null=True)
    language = models.CharField(max_length=500, null=True) 
    url_game = models.CharField(max_length=500, null=True)

    #si false -> partie pas encore commencé 
    started = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

class ArgumentParty(models.Model):
    name = models.CharField(max_length=500)
    value = models.CharField(max_length=500)
    type = models.CharField(max_length=500) 

    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='fk_game_argument')


class Participant(models.Model):
    party = models.ForeignKey(Party, related_name='participant_party', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='participant_player', on_delete=models.CASCADE)
    tag_player =  models.CharField(max_length=500, null=True)
    point = models.IntegerField(null=True)

    #Si false -> juste une invitation 
    accepting = models.BooleanField(default=False)


class Message(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message by {self.sender.username} in {self.party.title}'
    

class Play(models.Model):
    infoSend = models.CharField(max_length=5000)
    date_creation = models.DateTimeField(auto_now_add=True, null=True)

    #lien avec le joueur 
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='fk_game_partie')