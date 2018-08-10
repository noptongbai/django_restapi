from conclusion.models import ManufacturingTransaction, ManufacturingTransactionLine, Outage, PowerGeneration, \
    Consumtion
from transactions.models import Transaction, WithdrawDetail
from rest_framework.serializers import ModelSerializer
from  rest_framework import serializers
from  manufacturing_shifthead_serializers import ManufacturingTransactionSerializer
from mgpAPI.services.manu_withdraw_stock import manu_withdraw_stock
from datetime import datetime
from django.db import transaction
from  mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
import sys


class ConsumptionAllHeadSerializer(ModelSerializer):
    consumption_lines = ManufacturingTransactionSerializer(many=True)

    class Meta:
        model = Consumtion
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        print validated_data
        consumptions_data = validated_data.pop('consumption_lines')
        consumption = Consumtion.objects.create(title='mark')
        consumptions_data_check = consumptions_data

        for consumption_data in consumptions_data:
            lines_data = consumption_data.pop('lines')
            date = consumption_data["date"]
            menu_transaction = ManufacturingTransaction.objects.create(consumption=consumption,
                                                                       created_user=self.context['request'].user,
                                                                       last_modified_users=self.context['request'].user,
                                                                       **consumption_data)
            menu_transaction.created_date = date
            menu_transaction.date = date
            menu_transaction.save()

            for line_data in lines_data:
                manu_line = ManufacturingTransactionLine.objects.create(manufacturing_transaction=menu_transaction,
                                                                        created_user=self.context['request'].user,
                                                                        last_modified_users=self.context[
                                                                            'request'].user,
                                                                        **line_data)
                manu_line.created_date = date
                manu_line.save()

                if manu_line != None:

                    transaction = Transaction.objects.create(types=2, created_user=self.context['request'].user,
                                                             last_modified_users=self.context['request'].user,
                                                             date=datetime.now())
                    transaction.created_date = date
                    transaction.date = date
                    transaction.save()

                    track_data = {}
                    track_data["product"] = manu_line.product
                    track_data["quantity"] = manu_line.quantity
                    track_data["uom"] = manu_line.product.uom
                    track_data["sector"] = consumption_data["sector"]

                    if (manu_line.product.quantity >= manu_line.quantity):

                        withdraw_instance = WithdrawDetail.objects.create(transaction=transaction,
                                                                          created_user=self.context['request'].user,
                                                                          last_modified_users=self.context[
                                                                              'request'].user,
                                                                          **track_data)

                        withdraw_instance.created_date = date
                        withdraw_instance.save()

                        if withdraw_instance != None:
                            manu_withdraw_stock(track_data, withdraw_instance, manu_line, 1)
                            manu_line.withdraw = withdraw_instance
                            manu_line.save()

                    else:
                        raise serializers.ValidationError({"error": "not enough in stock"})

        if 'test' not in sys.argv:
            transaction_log_sync()
        return consumption
