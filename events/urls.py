from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('locations', views.LocationViewSet)
router.register("sectors", views.SectorViewSet)
router.register("event-sectors", views.EventSectorViewSet)
router.register("seats", views.SeatViewSet)
router.register("artists", views.ArtistViewSet)
router.register("genres", views.GenreViewSet)
router.register("tickets", views.TicketViewSet)
router.register("ticket-pools", views.TicketPoolViewSet)


urlpatterns = [
    path('events/', views.event_list, name='event-list'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),
]