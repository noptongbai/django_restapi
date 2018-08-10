from rest_framework.serializers import ModelSerializer
from  rest_framework import serializers


class ReportAll(object):
    def __init__(self, **kwargs):
        for field in ('categories', 'series', 'data'):
            setattr(self, field, kwargs.get(field, None))


class DataSerializer(serializers.Serializer):
    data = serializers.ListField(
        child=serializers.FloatField()
    )


class ReportAllSerializer(serializers.Serializer):
    categories = serializers.ListField(
        child=serializers.CharField(max_length=256)
    )
    series = serializers.ListField(
        DataSerializer
    )
