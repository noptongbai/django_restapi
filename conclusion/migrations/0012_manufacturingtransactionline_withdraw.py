# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-17 21:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_auto_20171017_2059'),
        ('conclusion', '0011_remove_manufacturingtransactionline_withdraw'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturingtransactionline',
            name='withdraw',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.WithdrawDetail'),
        ),
    ]
