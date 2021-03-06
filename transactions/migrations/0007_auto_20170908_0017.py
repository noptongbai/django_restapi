# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-08 00:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20170707_2026'),
        ('transactions', '0006_auto_20170908_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawdetail',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.Supplier'),
        ),
        migrations.AlterField(
            model_name='withdrawdetail',
            name='uom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='units.Unit'),
        ),
    ]
