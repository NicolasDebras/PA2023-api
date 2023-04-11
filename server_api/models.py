from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Player(AbstractUser):
    pass
    commentaire = models.CharField(max_length=50).empty_strings_allowed
