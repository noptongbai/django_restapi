# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-15 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conclusion', '0012_manufacturingtransactionline_withdraw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturingtransaction',
            name='consumption',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consumption_lines', to='conclusion.Consumtion'),
        ),
        migrations.AlterField(
            model_name='outage',
            name='consumption',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outage_lines', to='conclusion.Consumtion'),
        ),
        migrations.AlterField(
            model_name='powergeneration',
            name='consumption',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='generation_lines', to='conclusion.Consumtion'),
        ),
    ]
