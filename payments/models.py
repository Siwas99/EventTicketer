from email.policy import default
from random import choices
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from events.models import Event


# Create your models here.
class Order(models.Model):
    statuses = [
        ("", "ongoing"),
        ("Canceled" , "canceled"),
        ("Completed", "completed")
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(decimal_places=2)

    @property
    def total_amount(self):
        return self.unit_price * self.quantity


class Payment(models.Model):
    class Status(models.TextChoices):
        CREATED = "Created"
        PENDING = "Pending"
        PAID = "Paid"
        CANCELED = "Canceled"
        EXPIRED = "Expired"

    transaction_id = models.UUIDField(default=uuid4, unique=True)
    status = models.TextField(max_length=20, choices=Status.choices, default=Status.CREATED)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)