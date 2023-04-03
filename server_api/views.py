from .serializers import PlayerSerializers
from .models import Player
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def AllPlayerGet(request):
    res = Player.objects.all()
    serializers = PlayerSerializers(res, many=True)
    return Response(serializers.data)

#recupère un seul utilisateur 
@api_view(['GET'])
def PlayerGet(request, id):
    res = Player.objects.get(id=id)
    serializers = PlayerSerializers(res)
    return Response(serializers.data)

