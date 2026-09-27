from django.contrib import admin

from events.models import Event, Artist, Location, Genre, Ticket

# Register your models here.
admin.site.register(Location)
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Event)
admin.site.register(Ticket)
