from conclusion.models import ManufacturingTransaction, ManufacturingTransactionLine, Outage, PowerGeneration, \
    Consumtion
from rest_framework.serializers import ModelSerializer
from mgpAPI.serializers.manufacturing_shifthead_serializers import OutageSerializer
from django.db import transaction
from  rest_framework import serializers


class ConsumptionOutageSerializer(ModelSerializer):
    outage_lines = OutageSerializer(many=True)

    class Meta:
        model = Consumtion
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        outages_data = validated_data.pop('outage_lines')
        consumption = Consumtion.objects.create(title='mark')

        for outage_data in outages_data:
            Outage.objects.create(consumption=consumption,
                                  created_user=self.context['request'].user,
                                  last_modified_users=self.context['request'].user,
                                  **outage_data)

        return consumption
