from django.db import models

class User(models.Model):
    id = models.IntegerField()
    pseudo = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):
        return "{0} {{1}} [{2}]".format(self.id, self.pseudo, self.email)