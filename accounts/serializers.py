from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser
from events import serializers


class ListCustomUserSerializer(serializers.ModelSerializer):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "sex",
            "birth_date"
        )

class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "sex",
            "birth_date"
        )