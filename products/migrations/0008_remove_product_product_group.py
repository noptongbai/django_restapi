# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-14 15:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20171115_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_group',
        ),
    ]
