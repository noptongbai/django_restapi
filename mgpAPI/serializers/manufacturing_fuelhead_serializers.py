from conclusion.models import Consumtion
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from mgpAPI.services.withdraw_stock import withdraw_stock
from mgpAPI.services.input_stock import input_stock
from transactions.models import WithdrawDetail, Transaction, InputDetail
from common.master_models import Sector
from products.models import Product
from datetime import datetime
from mgpAPI.validator.validate_serializers import validate_check_unit_pk, validate_check_product_pk, \
    validate_check_sector_pk
from django.db import transaction
from  mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
import sys


class ChangeProductSerializer(serializers.Serializer):
    from_product = serializers.IntegerField(validators=[validate_check_product_pk])
    from_quantity = serializers.FloatField()
    from_unit = serializers.IntegerField(validators=[validate_check_unit_pk])
    to_product = serializers.IntegerField(validators=[validate_check_product_pk])
    to_quantity = serializers.FloatField()
    to_unit = serializers.IntegerField(validators=[validate_check_unit_pk])
    sector = serializers.IntegerField(validators=[validate_check_sector_pk])
    date = serializers.DateTimeField()


class ConsumptionFuelHeadSerializer(ModelSerializer):
    change_lines = ChangeProductSerializer(many=True, required=False)

    class Meta:
        model = Consumtion
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        consumptions_data_check = validated_data.get('change_lines')

        consumption = Consumtion.objects.create(title='mark')
        changes_datas = validated_data.pop('change_lines')

        for change_data in changes_datas:
            date = change_data.get('date')
            transaction = Transaction.objects.create(types=1, created_user=self.context['request'].user,
                                                     last_modified_users=self.context['request'].user,
                                                     date=datetime.now())
            transaction.created_date = date
            transaction.date = date
            transaction.save()

            product_instance1 = Product.objects.get(id=change_data["from_product"])
            product_instance2 = Product.objects.get(id=change_data["to_product"])
            sector = Sector.objects.get(id=change_data["sector"])
            track_data = {}
            track_data["product"] = product_instance1
            track_data["quantity"] = change_data["from_quantity"]
            track_data["uom"] = product_instance1.uom
            track_data["sector"] = sector

            withdraw_instance = WithdrawDetail.objects.create(transaction=transaction,
                                                              created_user=self.context['request'].user,
                                                              last_modified_users=self.context[
                                                                  'request'].user,
                                                              **track_data)
            withdraw_instance.created_date = date
            withdraw_instance.save()

            if withdraw_instance != None:
                withdraw = withdraw_stock(track_data, withdraw_instance, 1)

                transaction2 = Transaction.objects.create(types=0, created_user=self.context['request'].user,
                                                          last_modified_users=self.context['request'].user,
                                                          date=datetime.now())
                transaction2.created_date = date
                transaction2.date = date
                transaction2.save()

                track2_data = {}
                track2_data["product"] = product_instance2
                track2_data["quantity"] = change_data["to_quantity"]
                track2_data["uom"] = product_instance2.uom
                track2_data["unit_price"] = withdraw.unit_price

                input_instance = InputDetail.objects.create(transaction=transaction2,
                                                            created_user=self.context['request'].user,
                                                            last_modified_users=self.context['request'].user,
                                                            **track2_data)
                input_instance.created_date = date
                input_instance.save()

                if input_instance != None:
                    input_stock(track2_data, input_instance)

        if 'test' not in sys.argv:
            transaction_log_sync()
        return consumption
