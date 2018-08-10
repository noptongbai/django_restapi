from .models import Supplier
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
