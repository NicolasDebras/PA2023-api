from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Player(AbstractUser):
    commentaire = models.CharField(max_length=50).empty_strings_allowed

class Friend(models.Model): 
    Player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='friend1')
    Player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='friend2')

    #Si false -> juste une invitation 
    accepting = models.BooleanField(default=False)

class Party(models.Model): 
    title = models.CharField(max_length=50)
    Founder = models.ForeignKey(Player, related_name='founder', on_delete=models.CASCADE)
    url_image = models.CharField(max_length=500, null=True)

    #si false -> partie pas encore commencé 
    started = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


class Participant(models.Model):
    party = models.ForeignKey(Party, related_name='participant_party', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='participant_player', on_delete=models.CASCADE)

    #Si false -> juste une invitation 
    accepting = models.BooleanField(default=False)

 