from rest_framework.routers import DefaultRouter

from payments import views

router = DefaultRouter()

router.register('orders', views.OrderViewSet)
router.register('payments', views.PaymentViewSet)