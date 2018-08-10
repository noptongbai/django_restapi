from .models import Preferenc
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class PreferenceSerializer(ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'
