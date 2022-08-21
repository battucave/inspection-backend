from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import User

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','full_name', 'email','phone','password','user_type','is_verified')
        read_only = ('user_type','is_verified')
        ref_name = "AuthappUserCreateSerializer"

