from transactions.models import Transaction, InputDetail, TransactionLog
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from mgpAPI.services.input_stock import input_stock, update_stock
from  mgpAPI.validator.validate_serializers import validate_check_input_transaction_pk
from  mgpAPI.validator.validate_model import validate_nonzero
from  mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
import sys


class InputDetailSerializer(ModelSerializer):
    hard_delete = serializers.BooleanField(required=False)
    input_line_id = serializers.IntegerField(required=False, validators=[validate_check_input_transaction_pk])
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
    vendor_title = serializers.CharField(
        source='supplier.title',
        read_only=True
    )

    class Meta:
        model = InputDetail
        fields = (
            'id', 'product', 'uom', 'unit_price', 'amount', 'left_quantity', 'humidity', 'quantity', 'note',
            'created_date',
            'hard_delete',
            'supplier',
            'truck_license', 'input_line_id', 'stock_quantity', 'unit_title', 'product_title', 'vendor_title')


class TransactionSerializer(ModelSerializer):
    input_lines = InputDetailSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ('id', 'date', 'types', 'note', 'input_lines')

    def create(self, validated_data):
        tracks_data = validated_data.pop('input_lines')
        transaction = Transaction.objects.create(types=0, created_user=self.context['request'].user,
                                                 last_modified_users=self.context['request'].user, **validated_data)
        transaction.created_date = validated_data.get('date')
        transaction.save()

        for track_data in tracks_data:
            input_instance = InputDetail.objects.create(transaction=transaction,
                                                        created_user=self.context['request'].user,
                                                        last_modified_users=self.context['request'].user, **track_data)
            input_instance.created_date = validated_data["date"]
            input_instance.save()
            if input_instance != None:
                input_stock(track_data, input_instance)

        if 'test' not in sys.argv:
            transaction_log_sync()
        return transaction

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.note = validated_data.get('note', instance.note)
        instance.last_modified_users = self.context['request'].user
        instance.save()

        tracks_data = validated_data.pop('input_lines')

        for track_data in tracks_data:
            if track_data.get('input_line_id') == None:
                input_instance = InputDetail.objects.create(transaction=instance,
                                                            created_user=self.context['request'].user,
                                                            last_modified_users=self.context['request'].user,
                                                            **track_data)
                if input_instance != None:
                    input_stock(track_data, input_instance)

            elif (track_data.get('input_line_id') != None and track_data.get('hard_delete') == True):
                input_instance = InputDetail.objects.get(id=track_data.get('input_line_id'))
                if (input_instance.used == False):
                    TransactionLog.objects.get(input_transaction=input_instance).delete()
                    input_instance.delete()
                else:
                    raise serializers.ValidationError({"error": "Cant Edit this transaction already used"})
            else:
                input_instance = InputDetail.objects.get(id=track_data.get('input_line_id'))

                if (input_instance.used == False):
                    input_instance.truck_license = track_data.get("truck_license", input_instance.truck_license)
                    input_instance.description = track_data.get("description", input_instance.description)
                    input_instance.note = track_data.get("note", input_instance.note)
                    input_instance.supplier = track_data.get("supplier", input_instance.supplier)
                    input_instance.last_modified_users = self.context['request'].user
                    input_instance.save()

                    update_stock(track_data, input_instance)
                else:
                    raise serializers.ValidationError({"error": "Cant Edit this transaction already used"})
        return instance


class ReportInput(object):
    def __init__(self, **kwargs):
        for field in (
                'group', 'keys', 'nameEn'):
            setattr(self, field, kwargs.get(field, None))


class InputCostSerializer(serializers.Serializer):
    group = serializers.CharField(max_length=256)
    keys = serializers.CharField(max_length=256)
    nameEn = serializers.CharField(max_length=256)

class InputQuantitySerializer(serializers.Serializer):
    group = serializers.CharField(max_length=256)
    keys = serializers.CharField(max_length=256)
    nameEn = serializers.CharField(max_length=256)
