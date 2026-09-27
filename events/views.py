from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from events.models import Event, Location, Genre, Artist, Ticket
from events.serializers import EventSerializer, LocationSerializer, ArtistSerializer, GenreSerializer, \
    EventDetailSerializer, TicketSerializer, TicketDetailSerializer


@api_view(['GET', 'POST'])
def event_list(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=404)

    if request.method == "GET":
        serializer = EventDetailSerializer(event)
        return Response(serializer.data, status = 200)
    elif request.method == "PUT":
        serializer = EventSerializer(event, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    elif request.method == "DELETE":
        event.delete()
        return Response(status=204)

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TicketDetailSerializer

        return super().get_serializer_class()