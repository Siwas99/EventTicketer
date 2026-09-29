from django.contrib.auth.forms import UserCreationForm
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from accounts.models import CustomUser


class ListCustomUserSerializer(serializers.ModelSerializer):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
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
            "is_staff",
            "sex",
            "birth_date"
        )

class RegisterCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "sex",
            "birth_date"
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def validate(self, attrs):
        user = CustomUser(**attrs)
        try:
            validate_password(attrs['password'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({
                "password": exc.messages,
            })
        return attrs
