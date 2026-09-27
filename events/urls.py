from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    path('events/', views.event_list, name='event-list'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),
]