from django.conf import settings
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length = 100)
    country_code = models.CharField(max_length = 5)


    def __str__(self):
        return self.name + ' - ' + self.city

class Sector(models.Model):
    name = models.TextField(max_length=200)
    standing = models.BooleanField(),
    spots = models.PositiveIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

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

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    spots = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    artist = models.ManyToManyField(Artist)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tickets',
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        related_name="tickets",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username + ' - ' + self.event.name
