from django.db import models

from django.contrib.auth.models import User


class AuditModel(models.Model):
    created_user = models.ForeignKey(User, null=True, blank=True, related_name="create_user_%(class)s_objects")
    last_modified_users = models.ForeignKey(User, null=True,  blank=True,related_name="modified_user_%(class)s_objects")
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
