from django.db import models

# Create your models here.
class Player(models.Model):
    id = models.IntegerField().primary_key=True
    pseudo = models.CharField(max_length=25)
