from transactions.models import Transaction, ReturnDetail, InputJuntionReturn
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from mgpAPI.services.withdraw_stock import withdraw_stock
from mgpAPI.services.withdraw_stock_withoutfifo import withdraw_stock_withoutfifo
from  mgpAPI.validator.validate_serializers import validate_check_return_transaction_pk, \
    validate_check_input_transaction_pk
from django.db import transaction
from  mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
import sys


class InputArraySerializer(serializers.Serializer):
    id = serializers.IntegerField(validators=[validate_check_input_transaction_pk])
    qut = serializers.FloatField()


class InputJuntionReturnSerializer(ModelSerializer):
    vendor_title = serializers.CharField(
        source='supplier.title',
        read_only=True
    )

    class Meta:
        model = InputJuntionReturn
        fields = '__all__'


class ReturnDetailSerializer(ModelSerializer):
    return_input_lines = InputJuntionReturnSerializer(many=True, required=False)
    hard_delete = serializers.BooleanField(required=False)
    array = InputArraySerializer(many=True, required=False)
    return_line_id = serializers.IntegerField(required=False, validators=[validate_check_return_transaction_pk])
    stock_quantity = serializers.IntegerField(
        source='product.quantity',
        read_only=True
    )
    unit_title = serializers.CharField(
        source='uom.title',
        read_only=True
    )
    product_title = serializers.CharField(
        source='product.title',
        read_only=True
    )

    class Meta:
        model = ReturnDetail
        fields = (
            'id', 'product', 'uom', 'unit_price', 'humidity', 'quantity', 'note', 'hard_delete', 'supplier', 'amount',
            'supplier', 'array',
            'return_line_id', 'stock_quantity', 'unit_title', 'product_title', 'return_input_lines')


class TransactionSerializer(ModelSerializer):
    return_lines = ReturnDetailSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ('id', 'date', 'types', 'note', 'return_lines')

    @transaction.atomic
    def create(self, validated_data):
        consumptions_data_check = validated_data.get('return_lines')

        tracks_data = validated_data.pop('return_lines')
        transaction = Transaction.objects.create(types=3, created_user=self.context['request'].user,
                                                 last_modified_users=self.context['request'].user, **validated_data)
        transaction.created_date = validated_data["date"]
        transaction.save()

        for track_data in tracks_data:

            if track_data.get("array") != None:
                array = track_data.pop("array")
            else:
                array = None

            return_instance = ReturnDetail.objects.create(transaction=transaction,
                                                          created_user=self.context['request'].user,
                                                          last_modified_users=self.context['request'].user,
                                                          **track_data)
            return_instance.created_date = validated_data["date"]
            return_instance.save()

            if return_instance != None:
                if array != None:
                    withdraw_stock_withoutfifo(track_data, return_instance, 3, array)
                else:
                    withdraw_stock(track_data, return_instance, 3)

        if 'test' not in sys.argv:
            transaction_log_sync()
        return transaction
        # raise serializers.ValidationError("")

    # def update(self, instance, validated_data):
    #     instance.date = validated_data.get('date', instance.date)
    #     instance.note = validated_data.get('note', instance.note)
    #     instance.last_modified_users = self.context['request'].user
    #     instance.save()
    #
    #     tracks_data = validated_data.pop('return_lines')
    #
    #     for track_data in tracks_data:
    #         if track_data.get('return_line_id') == None:
    #             return_instance = ReturnDetail.objects.create(transaction=instance,
    #                                                           created_user=self.context['request'].user,
    #                                                           last_modified_users=self.context['request'].user,
    #                                                           **track_data)
    #             if return_instance != None:
    #                 withdraw_stock(track_data, return_instance, 3)
    #
    #         elif (track_data.get('return_line_id') != None and track_data.get('hard_delete') == True):
    #             ReturnDetail.objects.get(id=track_data.get('input_line_id')).delete()
    #         else:
    #             input_instance = ReturnDetail.objects.get(id=track_data.get('return_line_id'))
    #             input_instance.description = track_data.get("description", input_instance.description)
    #             input_instance.supplier = track_data.get("supplier", input_instance.supplier)
    #             input_instance.cost = track_data.get("cost", input_instance.cost)
    #             input_instance.product = track_data.get("product", input_instance.product)
    #             input_instance.unit = track_data.get("unit", input_instance.unit)
    #             input_instance.unit_cost = track_data.get("unit_cost", input_instance.unit_cost)
    #             input_instance.humidity = track_data.get("humidity", input_instance.humidity)
    #             input_instance.quantity = track_data.get("quantity", input_instance.quantity)
    #             input_instance.note = track_data.get("note", input_instance.note)
    #             input_instance.last_modified_users = self.context['request'].user
    #             input_instance.save()
    #     return instance
