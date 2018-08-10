# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-08 00:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_transactionlog_lines'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawdetail',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]
