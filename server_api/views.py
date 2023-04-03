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
    try:
        res = Player.objects.get(id=id)
    except:
        return Response(status=404)
    serializers = PlayerSerializers(res)
    return Response(serializers.data)

#Ajout un untilisateur 
@api_view(['POST'])
def PlayerAdd(request):
    serializers = PlayerSerializers(data = request.data)
    if serializers.is_valid():
        serializers.save()
    else:
        return Response(status=400)
    return Response(serializers.data)

@api_view(['PUT'])
def PlayerUpdate(request, id):
    try:
        res = Player.objects.get(id=id)
    except:
        return Response(status=404)
    serializers = PlayerSerializers(instance=res,data = request.data)
    if serializers.is_valid():
        serializers.save()
    else:
        return Response(status=400)
    return Response(serializers.data)

#delete un player
@api_view(['DELETE'])
def PlayerDelete(request, id):
    try:
        res = Player.objects.get(id=id)
    except:
        return Response(status=404)
    res.delete()
    return Response(status=200)