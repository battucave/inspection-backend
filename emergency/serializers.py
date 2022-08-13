from .models import Emergency 
from rest_framework import serializers


class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = "__all__"