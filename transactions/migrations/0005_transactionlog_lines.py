# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-16 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_auto_20170707_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionlog',
            name='lines',
            field=models.IntegerField(default=0),
        ),
    ]
