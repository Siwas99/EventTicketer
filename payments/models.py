from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "created"
        PENDING = "pending"
        SUCCEEDED = "succeeded"
        FAILED = "failed"
        CANCELLED = "cancelled"

    status = models.TextField(max_length=20, choices=Status, default=Status.CREATED)
    datetime = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @property
    def total_amount(self):
        return self.tickets.aggregate(
            total=models.Sum("purchase_price", default=0),
        )["total"]

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending"
        PAID = "paid"
        CANCELLED = "cancelled"
        EXPIRED = "expired"

    transaction_id = models.UUIDField(default=uuid4, unique=True)
    status = models.TextField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
