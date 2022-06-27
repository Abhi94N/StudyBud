from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        
    ]
    # can use jsonresponse but also fetch response using Response object
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    #Many=true to serialize a query set
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    rooms = Room.objects.get(id=pk)
    #Many=False to serialize one value
    serializer = RoomSerializer(rooms, many=False)
    return Response(serializer.data)