from conclusion.models import ManufacturingTransaction, ManufacturingTransactionLine, Outage, PowerGeneration, \
    Consumtion
from common.master_models import Sector
from transactions.models import WithdrawDetail, Transaction
from rest_framework.serializers import ModelSerializer
from mgpAPI.services.manu_withdraw_stock import manu_withdraw_stock
from datetime import datetime, timedelta
from rest_framework import serializers
from mgpAPI.daily_report_config.get_old_date import get_old_data
from  rest_framework import serializers
from common.master_models import Preference
from products.models import Product
from django.db import transaction
from  mgpAPI.erp_services.jounal_to_erp import transaction_log_sync
import sys


class ManufacturingTransactionLineSerializer(ModelSerializer):
    product_title = serializers.CharField(
        source='product.title',
        read_only=True
    )
    unit_title = serializers.CharField(
        source='unit.title',
        read_only=True
    )

    class Meta:
        model = ManufacturingTransactionLine
        fields = ('id', 'product', 'unit', 'quantity', 'product_title', 'unit_title')


class ManufacturingTransactionSerializer(ModelSerializer):
    lines = ManufacturingTransactionLineSerializer(many=True)
    date = serializers.DateTimeField(required=True)
    sector_title = serializers.CharField(
        source='sector.title',
        read_only=True
    )

    class Meta:
        model = ManufacturingTransaction
        fields = ('id', 'sector', 'date', 'note', 'lines', 'sector_title')


class ReportPowerGenerationSerializer(ModelSerializer):
    group = serializers.SerializerMethodField('get_group_product')
    keys = serializers.SerializerMethodField('get_key')
    company = serializers.SerializerMethodField('get_company_product')
    account = serializers.SerializerMethodField('get_account_product')
    chart = serializers.SerializerMethodField('get_type_product')
    type = serializers.SerializerMethodField('get_type_product')
    visibility = serializers.SerializerMethodField('get_type_product')

    def get_key(self, obj):
        return '{}{}'.format('MG', obj.id)

    def get_group_product(self, obj):
        return "Meter Power Generation"

    def get_company_product(self, obj):
        return "xxx"

    def get_account_product(self, obj):
        return "yyy"

    def get_type_product(self, obj):
        return 1

    class Meta:
        model = PowerGeneration
        fields = 'group', 'keys', 'company', 'account', 'chart', 'type', 'visibility', 'generate_meter'

class ReportPowerGenerationSerializerLast(ModelSerializer):

    class Meta:
        model = PowerGeneration
        fields = "__all__"


class OutageSerializer(ModelSerializer):
    class Meta:
        model = Outage
        fields = ('id', 'planned_outage', 'from_time', 'through_time', 'note')

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.planned_outage = validated_data.get('planned_outage', instance.planned_outage)
        instance.from_time = validated_data.get('from_time', instance.from_time)
        instance.through_time = validated_data.get('through_time', instance.through_time)
        instance.last_modified_users = self.context['request'].user
        instance.note = validated_data.get('note', instance.note)
        instance.save()
        return instance


class ReportOutageSerializer(ModelSerializer):
    group = serializers.SerializerMethodField('get_group_product')
    keys = serializers.SerializerMethodField('get_key')
    company = serializers.SerializerMethodField('get_company_product')
    account = serializers.SerializerMethodField('get_account_product')
    chart = serializers.SerializerMethodField('get_type_product')
    type = serializers.SerializerMethodField('get_type_product')
    visibility = serializers.SerializerMethodField('get_type_product')

    def get_key(self, obj):
        return '{}{}'.format('O', obj.id)

    def get_group_product(self, obj):
        return "Outage"

    def get_company_product(self, obj):
        return "xxx"

    def get_account_product(self, obj):
        return "yyy"

    def get_type_product(self, obj):
        return 1

    class Meta:
        model = Outage
        fields = 'group', 'keys', 'company', 'account', 'chart', 'type', 'visibility', 'planned_outage', 'from_time', 'through_time', 'note'


class ReportOutageVariabilitySerializer(ModelSerializer):
    group = serializers.SerializerMethodField('get_group_product')
    keys = serializers.SerializerMethodField('get_key')
    company = serializers.SerializerMethodField('get_company_product')
    account = serializers.SerializerMethodField('get_account_product')
    chart = serializers.SerializerMethodField('get_type_product')
    type = serializers.SerializerMethodField('get_type_product')
    visibility = serializers.SerializerMethodField('get_type_product')

    def get_key(self, obj):
        return '{}{}'.format('OV', obj.id)

    def get_group_product(self, obj):
        return "OutageVariability"

    def get_company_product(self, obj):
        return "xxx"

    def get_account_product(self, obj):
        return "yyy"

    def get_type_product(self, obj):
        return 1

    class Meta:
        model = Outage
        fields = 'group', 'keys', 'company', 'account', 'chart', 'type', 'visibility', 'planned_outage', 'from_time', 'through_time', 'note'


class ReportOutagePlannedSerializer(ModelSerializer):
    group = serializers.SerializerMethodField('get_group_product')
    keys = serializers.SerializerMethodField('get_key')
    company = serializers.SerializerMethodField('get_company_product')
    account = serializers.SerializerMethodField('get_account_product')
    chart = serializers.SerializerMethodField('get_type_product')
    type = serializers.SerializerMethodField('get_type_product')
    visibility = serializers.SerializerMethodField('get_type_product')

    def get_key(self, obj):
        return '{}{}'.format('OP', obj.id)

    def get_group_product(self, obj):
        return "OutagePlanned"

    def get_company_product(self, obj):
        return "xxx"

    def get_account_product(self, obj):
        return "yyy"

    def get_type_product(self, obj):
        return 1

    class Meta:
        model = Outage
        fields = 'group', 'keys', 'company', 'account', 'chart', 'type', 'visibility', 'planned_outage', 'from_time', 'through_time', 'note'


class ReportOutageUnplannedSerializer(ModelSerializer):
    group = serializers.SerializerMethodField('get_group_product')
    keys = serializers.SerializerMethodField('get_key')
    company = serializers.SerializerMethodField('get_company_product')
    account = serializers.SerializerMethodField('get_account_product')
    chart = serializers.SerializerMethodField('get_type_product')
    type = serializers.SerializerMethodField('get_type_product')
    visibility = serializers.SerializerMethodField('get_type_product')

    def get_key(self, obj):
        return '{}{}'.format('OU', obj.id)

    def get_group_product(self, obj):
        return "OutageUnplanned"

    def get_company_product(self, obj):
        return "xxx"

    def get_account_product(self, obj):
        return "yyy"

    def get_type_product(self, obj):
        return 1

    class Meta:
        model = Outage
        fields = 'group', 'keys', 'company', 'account', 'chart', 'type', 'visibility', 'planned_outage', 'from_time', 'through_time', 'note'


class PowerGenerationSerializerLast(ModelSerializer):
    class Meta:
        model = PowerGeneration
        fields = '__all__'


class PowerGenerationSerializer(ModelSerializer):
    accumulate_gross = serializers.SerializerMethodField('get_A')
    accumulate_net = serializers.SerializerMethodField('get_B')
    accumulate_mdb = serializers.SerializerMethodField('get_C')
    accumulate_auxilialy = serializers.SerializerMethodField('get_D')
    main_steam = serializers.SerializerMethodField('get_E')
    fuel_consumtion = serializers.SerializerMethodField('get_F')


    def get_A(self, obj):
        new, old = get_old_data(obj)
        if (old != None):
            data = new.generate_meter - old.generate_meter
        else:
            data = new.generate_meter
        return data

    def get_B(self, obj):
        new, old = get_old_data(obj)
        if (old != None):
            data = new.export_meter - old.export_meter
        else:
            data = new.export_meter
        return data

    def get_C(self, obj):
        new, old = get_old_data(obj)
        if (old != None):
            data = new.mdb_meter - old.mdb_meter
        else:
            data = new.mdb_meter
        return data

    def get_D(self, obj):
        new, old = get_old_data(obj)
        if (old != None):
            gross = new.generate_meter - old.generate_meter
            net = new.export_meter - old.export_meter
        else:
            gross = new.generate_meter
            net = new.export_meter
        data = gross - net
        return data

    def get_E(self, obj):
        power = PowerGeneration.objects.get(id=obj.id)
        try:
            pref = Preference.objects.get(key="steam_factor")
            value = float(pref.value)
        except Exception:
            value = 3.6
        return value * power.steam

    def get_F(self, obj):
        new, old = get_old_data(obj)
        if (old != None):
            data = new.weight_scale_meter - old.weight_scale_meter
        else:
            data = new.weight_scale_meter
        return data

    class Meta:
        model = PowerGeneration
        fields = 'id', 'sector', 'generate_meter', 'mdb_meter', 'export_meter', 'steam', 'weight_scale_meter', 'date', 'hours', 'accumulate_gross', 'accumulate_net', 'accumulate_mdb', 'accumulate_auxilialy', 'main_steam', 'fuel_consumtion'

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        print "yes"
        instance.sector = validated_data.get('sector', instance.sector)
        instance.generate_meter = validated_data.get('generate_meter', instance.generate_meter)
        instance.mdb_meter = validated_data.get('mdb_meter', instance.mdb_meter)
        instance.export_meter = validated_data.get('export_meter', instance.export_meter)
        instance.steam = validated_data.get('steam', instance.steam)
        instance.weight_scale_meter = validated_data.get('weight_scale_meter', instance.weight_scale_meter)
        instance.date = validated_data.get('date', instance.date)
        instance.generate_meter = validated_data.get('generate_meter', instance.generate_meter)
        instance.mdb_meter = validated_data.get('mdb_meter', instance.mdb_meter)
        instance.last_modified_users = self.context['request'].user
        instance.save()
        return instance


class MonitorPowerGenerationSerializer(ModelSerializer):
    accumulate_gross = serializers.SerializerMethodField('get_group_product')
    accumulate_net = serializers.SerializerMethodField('get_group_product')
    accumulate_auxilialy_power = serializers.SerializerMethodField('get_group_product')
    main_steam_consumption = serializers.SerializerMethodField('get_group_product')
    fuel_consumption = serializers.SerializerMethodField('get_group_product')

    class Meta:
        model = PowerGeneration
        fields = (
            'id', 'sector', 'generate_meter', 'mdb_meter', 'export_meter', 'steam', 'weight_scale_meter', 'date',
            'hours',
            'accumulate_gross', 'accumulate_net', 'accumulate_auxilialy_power', 'main_steam_consumption',
            'fuel_consumption')


class ReportPowerGenerationSerializer(ModelSerializer):
    group = serializers.SerializerMethodField('get_group_product')
    keys = serializers.SerializerMethodField('get_key')
    company = serializers.SerializerMethodField('get_company_product')
    account = serializers.SerializerMethodField('get_account_product')
    chart = serializers.SerializerMethodField('get_type_product')
    type = serializers.SerializerMethodField('get_type_product')
    visibility = serializers.SerializerMethodField('get_type_product')

    def get_key(self, obj):
        return '{}{}'.format('MG', obj.id)

    def get_group_product(self, obj):
        return "Meter Power Generation"

    def get_company_product(self, obj):
        return "xxx"

    def get_account_product(self, obj):
        return "yyy"

    def get_type_product(self, obj):
        return 1

    class Meta:
        model = PowerGeneration
        fields = 'group', 'keys', 'company', 'account', 'chart', 'type', 'visibility', 'generate_meter'


class ReportPowerExportSerializer(ModelSerializer):
    group = serializers.SerializerMethodField('get_group_product')
    keys = serializers.SerializerMethodField('get_key')
    company = serializers.SerializerMethodField('get_company_product')
    account = serializers.SerializerMethodField('get_account_product')
    chart = serializers.SerializerMethodField('get_type_product')
    type = serializers.SerializerMethodField('get_type_product')
    visibility = serializers.SerializerMethodField('get_type_product')

    def get_key(self, obj):
        return '{}{}'.format('ME', obj.id)

    def get_group_product(self, obj):
        return "Meter Power Export"

    def get_company_product(self, obj):
        return "xxx"

    def get_account_product(self, obj):
        return "yyy"

    def get_type_product(self, obj):
        return 1

    class Meta:
        model = PowerGeneration
        fields = 'group', 'keys', 'company', 'account', 'chart', 'type', 'visibility', 'export_meter'


class ReportPowerSteamSerializer(ModelSerializer):
    group = serializers.SerializerMethodField('get_group_product')
    keys = serializers.SerializerMethodField('get_key')
    company = serializers.SerializerMethodField('get_company_product')
    account = serializers.SerializerMethodField('get_account_product')
    chart = serializers.SerializerMethodField('get_type_product')
    type = serializers.SerializerMethodField('get_type_product')
    visibility = serializers.SerializerMethodField('get_type_product')

    def get_key(self, obj):
        return '{}{}'.format('MS', obj.id)

    def get_group_product(self, obj):
        return "Meter Steam Generation"

    def get_company_product(self, obj):
        return "xxx"

    def get_account_product(self, obj):
        return "yyy"

    def get_type_product(self, obj):
        return 1

    class Meta:
        model = PowerGeneration
        fields = 'group', 'keys', 'company', 'account', 'chart', 'type', 'visibility', 'steam'


class ConsumptionSerializer(ModelSerializer):
    generation_lines = PowerGenerationSerializer(many=True)
    consumption_lines = ManufacturingTransactionSerializer(many=True)
    outage_lines = OutageSerializer(many=True)

    class Meta:
        model = Consumtion
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        generations_data = validated_data.pop('generation_lines')
        consumptions_data = validated_data.pop('consumption_lines')
        outages_data = validated_data.pop('outage_lines')
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

                if len(PowerGeneration.objects.filter(created_date__lte=date, hours__lte=hour)) > 0:
                    print "yes"
                    stop = False

                    while stop != True:
                        try:
                            p = PowerGeneration.objects.get(created_date=date, hours=hour)

                            stop = True
                            stop2 = False
                            while stop2 != True:
                                if hour == 24:
                                    hour = 1
                                    date = date + timedelta(days=1)
                                else:
                                    hour = hour + 1
                                try:
                                    PowerGeneration.objects.get(created_date=date, hours=hour)
                                    stop2 = True
                                except Exception as E:
                                    power = PowerGeneration.objects.create(consumption=consumption,
                                                                           created_user=self.context['request'].user,
                                                                           last_modified_users=self.context[
                                                                               'request'].user,
                                                                           sector=p.sector)

                                    power.generate_meter = p.generate_meter
                                    power.mdb_meter = p.mdb_meter
                                    power.export_meter = p.export_meter
                                    power.steam = p.steam
                                    power.weight_scale_meter = p.weight_scale_meter
                                    power.created_date = date
                                    power.date = date
                                    power.hours = hour
                                    power.save()


                        except Exception as b:

                            if hour == 1:
                                hour = 24
                                date = date - timedelta(days=1)
                            else:
                                hour = hour - 1

        for outage_data in outages_data:
            Outage.objects.create(consumption=consumption,
                                  created_user=self.context['request'].user,
                                  last_modified_users=self.context['request'].user,
                                  **outage_data)

        for consumption_data in consumptions_data:
            lines_data = consumption_data.pop('lines')
            date = consumption_data.get('date')
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
