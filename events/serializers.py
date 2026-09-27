from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from events.models import Event, Location, Artist, Genre, Ticket


class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    date = serializers.DateTimeField()
    spots = serializers.IntegerField(min_value=0)
    price = serializers.DecimalField(max_digits=10, min_value=0, decimal_places=2)

    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all()
    )

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

class EventDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    date = serializers.DateTimeField()
    spots = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    location = LocationSerializer()
    artist = ArtistSerializer(many=True)

# IDK if this should not be exported to another app
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

class TicketDetailSerializer(serializers.Serializer):
    event = EventDetailSerializer(read_only=True)
    user = UserSerializer(read_only=True)