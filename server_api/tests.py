from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from .models import Player

class TestCategory(APITestCase):
    

    url = reverse_lazy('player')

    #voir bdd si possible de créer un env de test
    def test_list_player(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


    