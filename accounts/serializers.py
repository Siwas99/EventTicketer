from copy import copy

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

class CustomUserSerializer(serializers.ModelSerializer):
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
        password = attrs.get('password')

        if password is None:
            return attrs

        if self.instance is not None:
            user = copy(self.instance)
        else:
            user = CustomUser()

        for field, value in attrs.items():
            if field != "password":
                setattr(user, field, value)

        try:
            validate_password(password, user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({
                "password": exc.messages,
            })
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        if password is not None:
            instance.set_password(password)

        return super().update(instance, validated_data)

class AdminUserSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        fields = (
            "id",
            *CustomUserSerializer.Meta.fields,
            "is_staff",
        )
        read_only_fields = ("id",)
