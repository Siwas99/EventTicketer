from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from events.permissions import IsAdminOrReadOnly
from payments.models import Order, Payment
from payments.serializer import OrderSerializer, PaymentSerializer


# Create your views here.
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOrReadOnly]

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrReadOnly]