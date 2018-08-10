from conclusion.models import PowerGeneration, Consumtion
from rest_framework.serializers import ModelSerializer
from mgpAPI.serializers.manufacturing_shifthead_serializers import PowerGenerationSerializer
from  rest_framework import serializers
from django.db import transaction
from datetime import datetime, timedelta
from  mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
import sys

class ConsumptionGenerationSerializer(ModelSerializer):
    generation_lines = PowerGenerationSerializer(many=True)

    class Meta:
        model = Consumtion
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        generations_data = validated_data.pop('generation_lines')

        consumption = Consumtion.objects.create(title='mark')

        for generation_data in generations_data:
            a = PowerGeneration.objects.create(consumption=consumption,
                                               created_user=self.context['request'].user,
                                               last_modified_users=self.context['request'].user,
                                               **generation_data)
            a.created_date = generation_data.get('date')
            a.save()
            array_date = []

            for x in str(a.created_date.date()).split('-'):
                array_date.append(x)

            if len(PowerGeneration.objects.filter(created_date__year=array_date[0], created_date__month=array_date[1],
                                                  created_date__day=array_date[
                                                      2], hours=a.hours)) > 1:
                raise serializers.ValidationError({"error": "duplicate data"})
            else:
                hours = 0
                date = ''
                if a.hours == 1:
                    hour = 24
                    date = a.created_date - timedelta(days=1)
                else:
                    hour = a.hours - 1
                    date = a.created_date
                print PowerGeneration.objects.filter(created_date__lte=date, hours__lte=hour)
                if len(PowerGeneration.objects.filter(created_date__lte=date, hours__lte=hour)) > 0:
                    print "yes"
                    stop = False

                    while stop != True:
                        try:
                            PowerGeneration.objects.get(created_date=date, hours=hour)
                            stop = True
                            print "test"
                        except Exception as b:

                            power = PowerGeneration.objects.create(consumption=consumption,
                                                                   created_user=self.context['request'].user,
                                                                   last_modified_users=self.context['request'].user,
                                                                   **generation_data)

                            power.created_date = date
                            power.date = date
                            power.hours = hour
                            power.save()

                            if hour == 1:
                                hour = 24
                                date = date - timedelta(days=1)
                            else:
                                hour = hour - 1
        if 'test' not in sys.argv:
            transaction_log_sync()
        return consumption
