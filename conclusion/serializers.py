from .models import Shift
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class ShiftSerializer(ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'
