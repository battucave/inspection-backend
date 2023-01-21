from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import User
from django_rest_passwordreset.serializers import PasswordTokenSerializer
from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','full_name', 'email','phone','password','user_type','is_verified','profile_picture')
        read_only = ('user_type','is_verified')
        ref_name = "AuthappUserCreateSerializer"

class PasswordResetTokenSerializer(PasswordTokenSerializer):
    password2 = serializers.CharField(
        label=_("Password2"), style={"input_type": "password"}
    )

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise ValidationError("The Two passwords don't match")
        return super().validate(data)
