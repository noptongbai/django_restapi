from __future__ import unicode_literals
from django.db import models
from  common.utils_model import AuditModel


# Create your models here.
class Preference(AuditModel):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.key.encode('utf-8').strip()


class Sector(AuditModel):
    title = models.CharField(max_length=255, unique=True)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title.encode('utf-8').strip()


class Supplier(AuditModel):
    title = models.CharField(max_length=255, unique=True)
    ext_code = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.IntegerField(blank=True, null=True)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title.encode('utf-8').strip()
