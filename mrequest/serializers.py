from .models import MRequest
from rest_framework import serializers
from authapp.serializers import UserCreateSerializer


class MRequestSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(required=False)
    class Meta:
        model = MRequest
        fields = "__all__"

class MListRequestSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(required=False)
    class Meta:
        model = MRequest
        fields = "__all__"
    
  