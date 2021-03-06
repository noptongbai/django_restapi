# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-28 16:12
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import User
from units.models import UnitCategory


def load_user(apps, schema_editor):
    User.objects.create_superuser(username='admin', password='asdasdasd', email='admin@emal.com')


def load_sector(apps, schema_editor):
    sector = apps.get_model("common", "Sector")

    sector(title='shift test', description='shift test'
           ).save()


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_user), migrations.RunPython(load_sector),

    ]
