# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-15 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_title2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]