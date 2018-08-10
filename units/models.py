from __future__ import unicode_literals

from common.utils_model import AuditModel
from django.db import models
from mgpAPI.validator.validate_model import  validate_nonzero



class UnitCategory(AuditModel):
    title = models.CharField(max_length=255, unique=True)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title.encode('utf-8').strip()


class Unit(AuditModel):
    class Type(object):
        REFERENCE = 0
        SMALLER = 1
        BIGGER = 2

    TYPE_CHOICES = (
        (Type.REFERENCE, 'Reference'),
        (Type.SMALLER, 'Smaller'),
        (Type.BIGGER, 'Bigger'),
    )

    unit_category = models.ForeignKey(UnitCategory)
    title = models.CharField(max_length=255, unique=True)
    ext_code = models.CharField(max_length=255,null=True,blank=True)
    type = models.IntegerField(default=Type.REFERENCE, choices=TYPE_CHOICES)
    ratio = models.FloatField(default=1.0,validators=[validate_nonzero])
    timestamp = models.IntegerField( blank=True,null=True)

    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title.encode('utf-8').strip()



