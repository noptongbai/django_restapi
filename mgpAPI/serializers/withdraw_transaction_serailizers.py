from transactions.models import Transaction, WithdrawDetail, UnitCostHistory, TransactionLog
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from mgpAPI.services.withdraw_stock import withdraw_stock
from  mgpAPI.validator.validate_serializers import validate_check_withdraw_transaction_pk, validate_check_product_pk
from django.db import transaction
from  mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
import sys


class WithdrawDetailSerializer(ModelSerializer):
    hard_delete = serializers.BooleanField(required=False)
    withdraw_line_id = serializers.IntegerField(required=False, validators=[validate_check_withdraw_transaction_pk])
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
        model = WithdrawDetail
        fields = (
            'id', 'product', 'uom', 'unit_price', 'amount', 'humidity', 'quantity', 'note', 'hard_delete',
            'shift_head_user',
            'sector', 'withdrawer_name', 'withdraw_line_id', 'stock_quantity', 'unit_title', 'product_title')


class TransactionSerializer(ModelSerializer):
    withdraw_lines = WithdrawDetailSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ('id', 'date', 'types', 'note', 'withdraw_lines')

    @transaction.atomic
    def create(self, validated_data):

        consumptions_data_check = validated_data.get('withdraw_lines')

        tracks_data = validated_data.pop('withdraw_lines')

        transaction = Transaction.objects.create(types=1, created_user=self.context['request'].user,
                                                 last_modified_users=self.context['request'].user, **validated_data)
        transaction.created_date = validated_data["date"]
        transaction.save()
        for track_data in tracks_data:
            withdraw_instance = WithdrawDetail.objects.create(transaction=transaction,
                                                              created_user=self.context['request'].user,
                                                              last_modified_users=self.context['request'].user,
                                                              **track_data)
            withdraw_instance.created_date = validated_data["date"]
            withdraw_instance.save()

            if withdraw_instance != None:
                withdraw_stock(track_data, withdraw_instance, 1)

        if 'test' not in sys.argv:
            transaction_log_sync()
        return transaction
        # raise serializers.ValidationError("")

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.note = validated_data.get('note', instance.note)
        instance.last_modified_users = self.context['request'].user
        instance.save()

        tracks_data = validated_data.pop('withdraw_lines')

        for track_data in tracks_data:
            if track_data.get('withdraw_line_id') == None:
                withdraw_instance = WithdrawDetail.objects.create(transaction=instance,
                                                                  created_user=self.context['request'].user,
                                                                  last_modified_users=self.context['request'].user,
                                                                  **track_data)
                if withdraw_instance != None:
                    withdraw_stock(track_data, withdraw_instance, 1)

            elif (track_data.get('withdraw_line_id') != None and track_data.get('hard_delete') == True):
                WithdrawDetail.objects.get(id=track_data.get('withdraw_line_id')).delete()
            else:
                withdraw_instance = WithdrawDetail.objects.get(id=track_data.get('withdraw_line_id'))
                withdraw_instance.description = track_data.get("description", withdraw_instance.description)
                withdraw_instance.shift_head_user = track_data.get("shift_head_user", withdraw_instance.shift_head_user)
                withdraw_instance.amount = track_data.get("amount", withdraw_instance.amount)
                withdraw_instance.shift = track_data.get("shift", withdraw_instance.shift)
                withdraw_instance.product = track_data.get("product", withdraw_instance.product)
                withdraw_instance.uom = track_data.get("uom", withdraw_instance.uom)
                withdraw_instance.unit_cost = track_data.get("unit_cost", withdraw_instance.unit_cost)
                withdraw_instance.humidity = track_data.get("humidity", withdraw_instance.humidity)
                withdraw_instance.quantity = track_data.get("quantity", withdraw_instance.quantity)
                withdraw_instance.note = track_data.get("note", withdraw_instance.note)
                withdraw_instance.withdrawer_name = track_data.get("withdrawer_name", withdraw_instance.withdrawer_name)
                withdraw_instance.last_modified_users = self.context['request'].user
                withdraw_instance.save()
        return instance


class ReportWithdraw(object):
    def __init__(self, **kwargs):
        for field in (
                'group', 'keys', 'nameEn'):
            setattr(self, field, kwargs.get(field, None))


class WithdrawCostSerializer(serializers.Serializer):
    group = serializers.CharField(max_length=256)
    keys = serializers.CharField(max_length=256)
    nameEn = serializers.CharField(max_length=256)


class WithdrawQuantitySerializer(serializers.Serializer):
    group = serializers.CharField(max_length=256)
    keys = serializers.CharField(max_length=256)
    nameEn = serializers.CharField(max_length=256)
