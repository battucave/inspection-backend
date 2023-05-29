from property.serializers import PropertySerializer
from .models import Report
from rest_framework import serializers


class ReportSerializer(serializers.ModelSerializer):
    property = PropertySerializer(required=False)

    class Meta:
        model = Report
        fields = "__all__"