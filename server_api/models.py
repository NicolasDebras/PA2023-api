from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Player(AbstractUser):
    pass
    commentaire = models.CharField(max_length=50).empty_strings_allowed

class Friend(models.Model): 
    Player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='friend1')
    Player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='friend2')

    #Si false -> juste une invitation 
    accepting = models.BooleanField(default=False)
