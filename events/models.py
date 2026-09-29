from typing import cast

from django.conf import settings
from django.db import models
from django.db.models.functions import Coalesce


# LOCATION
class Location(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5)

    def __str__(self):
        return self.name + ' - ' + self.city


class Sector(models.Model):
    class Type(models.TextChoices):
        STAND = "Standing"
        SEAT = "SEATED"

    name = models.TextField(max_length=100)
    capacity = models.PositiveIntegerField()
    type = models.TextField(max_length=10, choices=Type, default=Type.STAND)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.location.name + " - " + self.name


class Seat(models.Model):
    name = models.TextField(max_length=100)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)


# ARTIST
class Genre(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=250)
    country = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)

    def __str__(self) -> str:
        return self.name


# EVENT
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    artist = models.ManyToManyField(Artist)

    def __str__(self):
        return self.name

    @property
    def total_capacity(self):
        return self.eventsector_set.aggregate(
            total=models.Sum(
                Coalesce("capacity", "sector__capacity"),
                default=0,
            )
        )["total"]


class EventSector(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints  = [
            models.UniqueConstraint(
                fields=["event", "sector"],
                name="unique_event_sector"
            ),
        ]

    @property
    def effective_capacity(self) -> int:
        capacity = cast(int | None, self.capacity)

        if capacity is not None:
            return capacity

        return self.sector.capacity

    def __str__(self):
        return self.event.name + ' - ' + self.sector.name

class TicketPool(models.Model):
    name = models.TextField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sector = models.ForeignKey(EventSector, on_delete=models.CASCADE)

class Ticket(models.Model):
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tickets',
        on_delete=models.CASCADE
    )
    ticket_pool = models.ForeignKey(
        TicketPool,
        related_name="tickets",
        on_delete=models.CASCADE
    )
    seat = models.ForeignKey(
        Seat,
        related_name="seat",
        on_delete=models.CASCADE,
        null=True
    ) # TODO Add in serializer check if seat is in ticket pool sector
    order = models.ForeignKey(
        "payments.Order",
        related_name="order",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username + ' - ' + self.ticket_pool.sector.event.name