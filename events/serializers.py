from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from events.models import Event, Location, Artist, Genre, Ticket, Sector, Seat, EventSector, TicketPool


class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    total_capacity = serializers.IntegerField(read_only=True)

    artist = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Artist.objects.all()
    )


    def create(self, validated_data: Any):
        artist = validated_data.pop('artist', None)

        event = Event.objects.create(**validated_data)
        event.artist.set(artist)

        return event

    def update(self, instance, validated_data):
        artist = validated_data.pop('artist', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        if artist is not None:
            instance.artist.set(artist)

        return instance


    # if serializer inherit from SerializerModel this would do the same
    # class Meta:
    #     model = Event
    #     fields = "__all__"



class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ArtistSerializer(ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class SectorSerializer(ModelSerializer):
    class Meta:
        model = Sector
        fields = "__all__"

class SeatSerializer(ModelSerializer):
    sector = serializers.PrimaryKeyRelatedField(
        queryset = Sector.objects.filter(
            type = Sector.Type.SEAT
        )
    )

    class Meta:
        model = Seat
        fields = "__all__"


class EventSectorSerializer(ModelSerializer):
    effective_capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = EventSector
        fields = "__all__"

    def validate(self, attrs):
        attrs = super().validate(attrs)

        event = attrs.get("event")
        sector = attrs.get("sector")

        if self.instance is not None:
            if event is None:
                event = self.instance.event
            if sector is None:
                sector = self.instance.sector

        other_sectors = EventSector.objects.filter(event=event)

        if self.instance is not None:
            other_sectors = other_sectors.exclude(pk=self.instance.pk)

        different_location_exists = other_sectors.exclude(
            sector__location_id=sector.location_id
        ).exists()

        if different_location_exists:
            raise serializers.ValidationError({
                "sector": ("All sectors must belong to the same location")
            })

        return attrs

class EventDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()

    artist = ArtistSerializer(many=True)

# IDK if this should not be exported to another app
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class TicketPoolSerializer(ModelSerializer):
    class Meta:
        model = TicketPool
        fields = "__all__"

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

class TicketDetailSerializer(serializers.Serializer):
    event = EventDetailSerializer(read_only=True)
    user = UserSerializer(read_only=True)