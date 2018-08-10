from transactions.models import Transaction, ScrapDetail, InputJuntionScrap
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from mgpAPI.services.withdraw_stock import withdraw_stock
from  mgpAPI.validator.validate_serializers import validate_check_input_transaction_pk, \
    validate_check_scrap_transaction_pk
from mgpAPI.services.withdraw_stock_withoutfifo import withdraw_stock_withoutfifo
from django.db import transaction
from  mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
import sys


class InputArraySerializer(serializers.Serializer):
    id = serializers.IntegerField(validators=[validate_check_input_transaction_pk])
    qut = serializers.FloatField()


class InputJuntionScrapSerializer(ModelSerializer):
    vendor_title = serializers.CharField(
        source='supplier.title',
        read_only=True
    )

    class Meta:
        model = InputJuntionScrap
        fields = '__all__'


class ScrapDetailSerializer(ModelSerializer):
    scrap_input_lines = InputJuntionScrapSerializer(many=True, required=False)
    hard_delete = serializers.BooleanField(required=False)
    array = InputArraySerializer(many=True, required=False)
    scrap_line_id = serializers.IntegerField(required=False, validators=[validate_check_scrap_transaction_pk])

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
        model = ScrapDetail
        fields = (
            'id', 'product', 'uom', 'unit_price', 'humidity', 'quantity', 'note', 'hard_delete', 'amount',
            'scrap_line_id', 'array', 'stock_quantity', 'unit_title', 'product_title', 'scrap_input_lines')


class TransactionSerializer(ModelSerializer):
    scrap_lines = ScrapDetailSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ('id', 'date', 'types', 'note', 'scrap_lines')

    @transaction.atomic
    def create(self, validated_data):
        consumptions_data_check = validated_data.get('scrap_lines')

        tracks_data = validated_data.pop('scrap_lines')
        transaction = Transaction.objects.create(types=2, created_user=self.context['request'].user,
                                                 last_modified_users=self.context['request'].user, **validated_data)
        transaction.created_date = validated_data["date"]
        transaction.save()

        for track_data in tracks_data:
            if track_data.get("array") != None:
                array = track_data.pop("array")
            else:
                array = None

            scrap_instance = ScrapDetail.objects.create(transaction=transaction,
                                                        created_user=self.context['request'].user,
                                                        last_modified_users=self.context['request'].user, **track_data)
            scrap_instance.created_date = validated_data["date"]
            scrap_instance.save()

            if scrap_instance != None:
                if array != None:
                    withdraw_stock_withoutfifo(track_data, scrap_instance, 2, array)
                else:
                    withdraw_stock(track_data, scrap_instance, 2)

        if 'test' not in sys.argv:
            transaction_log_sync()
        return transaction
        # raise serializers.ValidationError("")

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.note = validated_data.get('note', instance.note)
        instance.last_modified_users = self.context['request'].user
        instance.save()

        tracks_data = validated_data.pop('scrap_lines')

        for track_data in tracks_data:
            if track_data.get('scrap_line_id') == None:
                scrap_instance = ScrapDetail.objects.create(transaction=instance,
                                                            created_user=self.context['request'].user,
                                                            last_modified_users=self.context['request'].user,
                                                            **track_data)
                if scrap_instance != None:
                    withdraw_stock(track_data, scrap_instance, 2)

            elif (track_data.get('scrap_line_id') != None and track_data.get('hard_delete') == True):
                ScrapDetail.objects.get(id=track_data.get('scrap_line_id')).delete()
            else:
                input_instance = ScrapDetail.objects.get(id=track_data.get('scrap_line_id'))
                input_instance.description = track_data.get("description", input_instance.description)
                input_instance.cost = track_data.get("cost", input_instance.cost)
                input_instance.product = track_data.get("product", input_instance.product)
                input_instance.unit = track_data.get("unit", input_instance.unit)
                input_instance.unit_cost = track_data.get("unit_cost", input_instance.unit_cost)
                input_instance.humidity = track_data.get("humidity", input_instance.humidity)
                input_instance.quantity = track_data.get("quantity", input_instance.quantity)
                input_instance.note = track_data.get("note", input_instance.note)
                input_instance.last_modified_users = self.context['request'].user
                input_instance.save()
        return instance
