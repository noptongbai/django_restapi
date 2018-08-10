from rest_framework.serializers import ModelSerializer
from  rest_framework import serializers


class ReportDaily(object):
    def __init__(self, **kwargs):
        for field in ('date', 'energy_hours', 'energy_dates', 'products_consumption', 'generation', 'outages'):
            setattr(self, field, kwargs.get(field, None))


class OutageSerializer(serializers.Serializer):
    planned_outage = serializers.CharField(max_length=255)
    note = serializers.CharField(max_length=255)
    from_time = serializers.DateTimeField()
    through_time = serializers.DateTimeField()


class ConsumtionSerializer(serializers.Serializer):
    product = serializers.CharField(max_length=255)
    unit = serializers.CharField(max_length=255)
    quantity = serializers.FloatField()


class GenerationSerializer(serializers.Serializer):
    sector = serializers.CharField(max_length=255)
    generate_meter = serializers.IntegerField()
    mdb_meter = serializers.IntegerField()
    export_meter = serializers.IntegerField()
    steam = serializers.FloatField()
    weight_scale_meter = serializers.IntegerField()
    date = serializers.DateTimeField()


class EnergyHourSerializer(serializers.Serializer):
    hour = serializers.IntegerField()
    accumulate_net = serializers.FloatField()
    accumulate_gross = serializers.FloatField()
    main_steam_consumption = serializers.FloatField()

class EnergyDateSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    accumulate_net = serializers.FloatField()
    accumulate_gross = serializers.FloatField()
    main_steam_consumption = serializers.FloatField()


class ReportDailyDateSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    energy_hours = serializers.ListField(
        EnergyHourSerializer
    )
    energy_dates = serializers.ListField(
        EnergyDateSerializer
    )
    products_consumption = serializers.ListField(
        ConsumtionSerializer
    )
    generation = serializers.ListField(
        GenerationSerializer
    )
    outages = serializers.ListField(
        OutageSerializer
    )
