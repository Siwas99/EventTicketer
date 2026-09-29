from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    sexes = [
        ('M', "Male"),
        ('F', "Female")
    ]

    sex = models.CharField(max_length=2, choices=sexes)
    birth_date = models.DateField()

    REQUIRED_FIELDS = ["email", "sex", "birth_date"]

