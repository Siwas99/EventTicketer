from random import randint

from django.db import transaction
from django.db.models import Count, F
from django.db.models.base import Model
from django.db.models.functions import Coalesce

from events.models import Event, EventSector, Seat, TicketPool, Ticket, Sector
from payments.models import Order


#
# def get_random_event_with_free_slots():
#     return EventSector.objects.annotate(
#         ticket_count = Count("ticketpool__tickets"),
#         capacity_limit = Coalesce("capacity", "sector__capacity"),
#     ).filter(capacity_limit__gt=F("ticket_count")).order_by('?').first()
#
def get_random_free_seat(event_sector: EventSector) -> Seat | None:
    taken_seat_ids = Ticket.objects.filter(
        ticket_pool__sector=event_sector,
        seat__isnull=False,
    ).values('seat_id')

    return (
        Seat.objects
        .filter(sector_id=event_sector.sector_id)
        .exclude(pk__in=taken_seat_ids)
        .order_by('?')
        .first()
    )


class NoTicketAvailable(Exception):
    pass

def get_available_event_sectors():
    return (
        EventSector.objects.filter(
            ticketpool__isnull=False
        ).annotate(
            ticket_count=Count('ticketpool__tickets'),
            capacity_limit=Coalesce("capacity", "sector__capacity")
        ).filter(capacity_limit__gt=F("ticket_count"))
    )

@transaction.atomic
def try_create_ticket(user, event_sector_id: int) -> Ticket | None:
    event_sector = (
        EventSector.objects
        .select_for_update()
        .filter(pk=event_sector_id)
        .first()
    )

    if event_sector is None:
        return None

    ticket_count = Ticket.objects.filter(
        ticket_pool__sector=event_sector,
    ).count()

    if ticket_count >= event_sector.effective_capacity:
        return None

    ticket_pool = (
        TicketPool.objects
        .filter(sector=event_sector)
        .order_by("?")
        .first()
    )

    if ticket_pool is None:
        return None

    seat = None

    if event_sector.sector.type == Sector.Type.SEAT:
        seat = get_random_free_seat(event_sector)

        if seat is None:
            return None

    order = Order.objects.create(user=user)

    return Ticket.objects.create(
        order=order,
        user=user,
        ticket_pool=ticket_pool,
        purchase_price=ticket_pool.price,
        seat=seat,
    )

def create_random_ticket(user):
    sector_ids = list(
        get_available_event_sectors()
        .values_list("pk", flat=True)
    )

    for sector_id in sector_ids:
        ticket = try_create_ticket(user, sector_id)

        if ticket is not None:
            return ticket

    raise NoTicketAvailable("No tickets available")