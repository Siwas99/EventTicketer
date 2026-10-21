from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from events.permissions import IsAdminOrReadOnly
from payments.models import Order, Payment
from payments.serializer import OrderSerializer, PaymentSerializer


# Create your views here.
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user
        if user.is_staff:
            return queryset
        return queryset.filter(user = self.request.user)

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user
        if user.is_staff:
            return queryset
        return queryset.filter(order__user = self.request.user)