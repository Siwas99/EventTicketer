from django.db.utils import DatabaseError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import ModelViewSet

from events.models import Event, Location, Genre, Artist, Ticket, Sector, Seat, EventSector, TicketPool
from events.permissions import IsAdminOrReadOnly
from events.serializers import EventSerializer, LocationSerializer, ArtistSerializer, GenreSerializer, \
    EventDetailSerializer, TicketSerializer, TicketDetailSerializer, SectorSerializer, SeatSerializer, \
    EventSectorSerializer, TicketPoolSerializer
from events.services import create_random_ticket, NoTicketAvailable


@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
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
@permission_classes([IsAdminOrReadOnly])
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
    permission_classes = [IsAdminOrReadOnly]

class SectorViewSet(ModelViewSet):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAdminOrReadOnly]

class SeatViewSet(ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAdminOrReadOnly]

class EventSectorViewSet(ModelViewSet):
    queryset = EventSector.objects.all()
    serializer_class = EventSectorSerializer
    permission_classes = [IsAdminOrReadOnly]

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAdminOrReadOnly]

class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TicketDetailSerializer

        return super().get_serializer_class()

    @action(
        detail=False,
        methods=['POST'],
        url_path="random",
        permission_classes=[IsAuthenticated]
    )
    def get_random_ticket(self, request):
        try:
            ticket = create_random_ticket(user=request.user)

        except NoTicketAvailable as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_409_CONFLICT
            )

        except DatabaseError:
            return Response(
                {"detail": "Ticket creating failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = self.get_serializer(ticket)
        return Response(serializer.data, status=HTTP_201_CREATED)

class TicketPoolViewSet(ModelViewSet):
    queryset = TicketPool.objects.all()
    serializer_class = TicketPoolSerializer
    permission_classes = [IsAdminOrReadOnly]

