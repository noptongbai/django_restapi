from __future__ import unicode_literals

from django.db import models
from datetime import date, datetime
from products.models import Product
from  common.master_models import Sector
from  common.utils_model import AuditModel
from units.models import Unit
from transactions.models import WithdrawDetail


class Consumtion(models.Model):
    title = models.CharField(max_length=255, default="pk")


class PowerGeneration(AuditModel):
    consumption = models.ForeignKey(Consumtion, related_name='generation_lines', null=True, blank=True)
    sector = models.ForeignKey(Sector)
    generate_meter = models.PositiveIntegerField(default=0)
    mdb_meter = models.PositiveIntegerField(default=0)
    export_meter = models.PositiveIntegerField(default=0)
    steam = models.FloatField(default=0)
    weight_scale_meter = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)
    hours = models.IntegerField(default=0)
    soft_delete = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Date: ' + str(self.created_date) + ' Hours: ' + str(self.hours)


class Outage(AuditModel):
    class Type(object):
        PLAN = 0
        UNPLAN = 1
        VARIABILITY = 2

    TYPE_CHOICES = (
        (Type.PLAN, 'plan'),
        (Type.UNPLAN, 'unplan'),
        (Type.VARIABILITY, 'variability')
    )
    consumption = models.ForeignKey(Consumtion, related_name='outage_lines', null=True, blank=True)
    planned_outage = models.IntegerField(default=Type.PLAN, choices=TYPE_CHOICES)
    note = models.CharField(max_length=255, null=True, blank=True)
    from_time = models.DateTimeField()
    through_time = models.DateTimeField()
    soft_delete = models.BooleanField(default=False)


class ManufacturingTransaction(AuditModel):
    consumption = models.ForeignKey(Consumtion, related_name='consumption_lines', null=True, blank=True)
    sector = models.ForeignKey(Sector)
    date = models.DateTimeField(default=datetime.now, blank=True)
    note = models.TextField(null=True, blank=True)
    soft_delete = models.BooleanField(default=False)


class ManufacturingTransactionLine(AuditModel):
    manufacturing_transaction = models.ForeignKey(ManufacturingTransaction, related_name='lines')
    withdraw = models.ForeignKey(WithdrawDetail, null=True, blank=True)
    product = models.ForeignKey(Product)
    unit = models.ForeignKey(Unit)
    quantity = models.FloatField(default=0.00)
