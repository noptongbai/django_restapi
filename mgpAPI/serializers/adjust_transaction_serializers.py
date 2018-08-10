from transactions.models import Transaction, AdjustDetail, TransactionLog, InputJuntionAdjust
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from mgpAPI.services.adjust_calculate import adjust_input_stock, update_adjust_stock
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


class InputJuntionAdjustSerializer(ModelSerializer):
    vendor_title = serializers.CharField(
        source='supplier.title',
        read_only=True
    )

    class Meta:
        model = InputJuntionAdjust
        fields = '__all__'


class AdjustDetailSerializer(ModelSerializer):
    adjust_input_lines = InputJuntionAdjustSerializer(many=True, required=False)
    hard_delete = serializers.BooleanField(required=False)
    array = InputArraySerializer(many=True, required=False)
    adjust_line_id = serializers.IntegerField(required=False)
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
        model = AdjustDetail
        fields = ('id', 'product', 'uom', 'amount', 'unit_price', 'humidity', 'quantity', 'note', 'hard_delete', 'array'
                  , 'adjust_line_id', 'stock_quantity', 'unit_title', 'product_title', 'adjust_input_lines')


class TransactionSerializer(ModelSerializer):
    adjust_lines = AdjustDetailSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ('id', 'date', 'types', 'note', 'adjust_lines')

    @transaction.atomic
    def create(self, validated_data):
        consumptions_data_check = validated_data.get('adjust_lines')

        tracks_data = validated_data.pop('adjust_lines')
        transaction = Transaction.objects.create(types=4, created_user=self.context['request'].user,
                                                 last_modified_users=self.context['request'].user, **validated_data)
        transaction.created_date = validated_data["date"]
        transaction.save()

        for track_data in tracks_data:

            if track_data.get("array") != None:
                array = track_data.pop("array")
                if track_data.get("quantity") != None:
                    track_data.pop("quantity")
            else:
                array = None

            adjust_instance = AdjustDetail.objects.create(transaction=transaction,
                                                          created_user=self.context['request'].user,
                                                          last_modified_users=self.context['request'].user,
                                                          **track_data)
            adjust_instance.created_date = validated_data["date"]
            adjust_instance.save()

            if adjust_instance != None:
                if (adjust_instance.quantity > 0):
                    adjust_input_stock(track_data, adjust_instance, self.context['request'].user, transaction.date)
                else:
                    if array != None:
                        withdraw_stock_withoutfifo(track_data, adjust_instance, 4, array)
                    else:
                        track_data["quantity"] = - track_data["quantity"]
                        withdraw_stock(track_data, adjust_instance, 4)

        if 'test' not in sys.argv:
            transaction_log_sync()
        return transaction

    # def update(self, instance, validated_data):
    #     instance.date = validated_data.get('date', instance.date)
    #     instance.note = validated_data.get('note', instance.note)
    #     instance.last_modified_users = self.context['request'].user
    #     instance.save()
    #
    #     tracks_data = validated_data.pop('adjust_lines')
    #
    #     for track_data in tracks_data:
    #         if track_data.get('adjust_line_id') == None:
    #             adjust_instance = AdjustDetail.objects.create(transaction=instance,
    #                                                           created_user=self.context['request'].user,
    #                                                           last_modified_users=self.context['request'].user,
    #                                                           **track_data)
    #             if adjust_instance != None:
    #                 adjust_stock(track_data, adjust_instance)
    #
    #         elif (track_data.get('adjust_line_id') != None and track_data.get('hard_delete') == True):
    #             adjust_instance = AdjustDetail.objects.get(id=track_data.get('adjust_line_id'))
    #             TransactionLog.objects.get(adjust_transaction=adjust_instance).delete()
    #             adjust_instance.delete()
    #         else:
    #             adjust_instance = AdjustDetail.objects.get(id=track_data.get('adjust_line_id'))
    #             adjust_instance.description = tracks_data.get("description", adjust_instance.description)
    #             adjust_instance.product = track_data.get("product", adjust_instance.product)
    #             adjust_instance.uom = track_data.get("uom", adjust_instance.unit)
    #             adjust_instance.quantity = track_data.get("quantity", adjust_instance.quantity)
    #             adjust_instance.note = track_data.get("note", adjust_instance.note)
    #             adjust_instance.last_modified_users = self.context['request'].user
    #             adjust_instance.save()
    #
    #             update_adjust_stock(track_data, adjust_instance)
    #     return instance
