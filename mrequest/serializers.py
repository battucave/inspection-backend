from .models import MRequest
from rest_framework import serializers
from authapp.serializers import UserCreateSerializer


class MRequestSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(required=False)
    class Meta:
        model = MRequest
        fields = "__all__"
        extra_kwargs = { 'request_name': { 'required': False }, 'description': { 'required': False }, 'request_state': { 'required': False } }

class MListRequestSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(required=False)
    class Meta:
        model = MRequest
        fields = "__all__"
    
  