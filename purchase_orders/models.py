from __future__ import unicode_literals

from django.db import models
from products.models import Product
from units.models import Unit
from common.master_models import Supplier
from common.utils_model import AuditModel


class PurchaseOrder(AuditModel):
    po = models.CharField(max_length=255)
    posting_date = models.DateTimeField()
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    timestamp = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.po.encode('utf-8').strip()


class PurchaseOrderLine(AuditModel):

    class Type(object):
        OPENED = 0
        PARTIAL = 1
        DELIVERED = 2

    TYPE_CHOICES = (
        (Type.OPENED, 'Opened'),
        (Type.PARTIAL, 'Partial'),
        (Type.DELIVERED, 'Delivered'),
    )
    purchase_orders = models.ForeignKey(PurchaseOrder)
    product = models.ForeignKey(Product, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, null=True, blank=True)
    delivered = models.IntegerField(default=Type.OPENED, choices=TYPE_CHOICES)
    uom = models.ForeignKey(Unit, null=True, blank=True)
    line_no = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.FloatField(default=0)
    outstanding_quantity = models.FloatField(default=0)
    unit_cost = models.FloatField(default=0)
    soft_delete = models.BooleanField(default=False)
    timestamp = models.IntegerField(blank=True, null=True)
