from __future__ import unicode_literals

from django.db import models
from units.models import Unit
from  common.utils_model import AuditModel
from django.contrib.auth.models import Group


class ProductCategory(AuditModel):
    title = models.CharField(max_length=255)
    ext_code = models.CharField(max_length=255, null=True, blank=True)
    soft_delete = models.BooleanField(default=False)
    humidity_type = models.BooleanField(default=False)
    shift_head_able = models.BooleanField(default=False)
    item_category_code = models.CharField(max_length=255, null=True, blank=True)
    erp_type = models.BooleanField(default=False)
    timestamp = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title.encode('utf-8').strip()


class Product(AuditModel):
    uom = models.ForeignKey(Unit)
    product_category = models.ForeignKey(ProductCategory, null=True, blank=True)
    ext_code = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    title2 = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.FloatField(default=0.0)
    valuation = models.FloatField(default=0.0)
    stockable = models.BooleanField(default=True)
    erp_type = models.BooleanField(default=False)
    soft_delete = models.BooleanField(default=False)
    timestamp = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title.encode('utf-8').strip()


class ProductLedger(AuditModel):
    entry_no = models.IntegerField()
    ext_code = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.FloatField(default=0.0)
    timestamp = models.IntegerField(blank=True, null=True)
