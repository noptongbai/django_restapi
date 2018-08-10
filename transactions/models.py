from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from common.utils_model import AuditModel
from  common.master_models import Supplier, Sector
from products.models import Product
from units.models import Unit
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Transaction(AuditModel):
    class Type(object):
        INPUT = 0
        WITHDRAW = 1
        SCRAP = 2
        RETURN = 3
        ADJUSTMENT = 4

    TYPE_CHOICES = (
        (Type.INPUT, 'Input'),
        (Type.WITHDRAW, 'Withdraw'),
        (Type.SCRAP, 'Scrap'),
        (Type.RETURN, 'Return'),
        (Type.ADJUSTMENT, 'Adjustment')
    )
    date = models.DateTimeField(null=True, blank=True)
    types = models.IntegerField(default=Type.INPUT, choices=TYPE_CHOICES)
    note = models.TextField(null=True, blank=True)
    po = models.CharField(max_length=255, null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    erp_type = models.BooleanField(default=False)
    erp_no = models.IntegerField(default=0)
    timestamp = models.IntegerField(blank=True, null=True)


class TransactionLineModel(AuditModel):
    product = models.ForeignKey(Product)
    quantity = models.FloatField(default=0.0)
    uom = models.ForeignKey(Unit)
    unit_price = models.FloatField(default=0.0)
    amount = models.FloatField(default=0)
    humidity = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    erp_no = models.IntegerField(default=0)
    note = models.TextField(null=True, blank=True)


    class Meta:
        abstract = True


class InputDetail(TransactionLineModel):
    transaction = models.ForeignKey(Transaction, related_name="input_lines")
    product = models.ForeignKey(Product, null=True, blank=True)
    uom = models.ForeignKey(Unit, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    truck_license = models.CharField(max_length=255, null=True, blank=True)
    weighing_card = models.CharField(max_length=255, null=True, blank=True)
    humidity_converted = models.FloatField(default=0)
    left_quantity = models.FloatField(default=0)
    reserve_quantity = models.FloatField(default=0)
    erp_type = models.BooleanField(default=False)
    timestamp = models.IntegerField(blank=True, null=True)


# Create your models here.
class WithdrawDetail(TransactionLineModel):
    transaction = models.ForeignKey(Transaction, related_name="withdraw_lines")
    shift_head_user = models.ForeignKey(User, null=True, blank=True)
    sector = models.ForeignKey(Sector, null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True)
    uom = models.ForeignKey(Unit, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    erp_type = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    withdrawer_name = models.TextField(null=True, blank=True)
    check = models.BooleanField(default=False)


class ScrapDetail(TransactionLineModel):
    transaction = models.ForeignKey(Transaction, related_name="scrap_lines")


class AdjustDetail(TransactionLineModel):
    transaction = models.ForeignKey(Transaction, related_name="adjust_lines")


class ReturnDetail(TransactionLineModel):
    transaction = models.ForeignKey(Transaction, related_name="return_lines")
    supplier = models.ForeignKey(Supplier, null=True, blank=True)


class UnitCostHistory(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    unit_price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)


class InputJuntionModel(models.Model):
    input_transaction = models.ForeignKey(InputDetail)
    quantity = models.FloatField(default=0)
    date = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)

    class Meta:
        abstract = True


class InputJuntionWithdraw(InputJuntionModel):
    withdraw_transaction = models.ForeignKey(WithdrawDetail)


class InputJuntionScrap(InputJuntionModel):
    scrap_transaction = models.ForeignKey(ScrapDetail, related_name="scrap_input_lines")


class InputJuntionReturn(InputJuntionModel):
    return_transaction = models.ForeignKey(ReturnDetail, related_name="return_input_lines")


class InputJuntionAdjust(InputJuntionModel):
    adjust_transaction = models.ForeignKey(AdjustDetail, related_name="adjust_input_lines")


class TransactionLog(AuditModel):
    product = models.ForeignKey(Product)
    uom = models.ForeignKey(Unit)
    name = models.CharField(max_length=255)
    input_transaction = models.ForeignKey(InputDetail, null=True, blank=True)
    withdraw_transaction = models.ForeignKey(WithdrawDetail, null=True, blank=True)
    scrap_transaction = models.ForeignKey(ScrapDetail, null=True, blank=True)
    return_transaction = models.ForeignKey(ReturnDetail, null=True, blank=True)
    adjust_transaction = models.ForeignKey(AdjustDetail, null=True, blank=True)
    unit_price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    lines = models.IntegerField(default=0)
    synced = models.BooleanField(default=False)
