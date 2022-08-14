from .models import MRequest
from rest_framework import serializers


class MRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MRequest
        fields = "__all__"