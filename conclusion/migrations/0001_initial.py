# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-02 13:43
from __future__ import unicode_literals

import common.master_models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumtion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='pk', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ManufacturingTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('sector', models.IntegerField(verbose_name=common.master_models.Sector)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('note', models.TextField(blank=True, null=True)),
                ('soft_delete', models.BooleanField(default=False)),
                ('consumption', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumption_lines', to='conclusion.Consumtion')),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_manufacturingtransaction_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_manufacturingtransaction_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ManufacturingTransactionLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('received_quantity', models.FloatField(default=0.0)),
                ('used_quantity', models.FloatField(default=0.0)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_manufacturingtransactionline_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_manufacturingtransactionline_objects', to=settings.AUTH_USER_MODEL)),
                ('manufacturing_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='conclusion.ManufacturingTransaction')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.Unit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Outage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('planned_outage', models.IntegerField(choices=[(0, 'plan'), (1, 'unplan'), (2, 'variability')], default=0)),
                ('note', models.CharField(max_length=255)),
                ('from_time', models.DateTimeField()),
                ('through_time', models.DateTimeField()),
                ('soft_delete', models.BooleanField(default=False)),
                ('consumption', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outage_lines', to='conclusion.Consumtion')),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_outage_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_outage_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PowerGeneration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('sector', models.IntegerField(verbose_name=common.master_models.Sector)),
                ('generate_meter', models.PositiveIntegerField(default=0)),
                ('mdb_meter', models.PositiveIntegerField(default=0)),
                ('export_meter', models.PositiveIntegerField(default=0)),
                ('steam', models.FloatField(default=0)),
                ('weight_scale_meter', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('hours', models.IntegerField(default=0)),
                ('soft_delete', models.BooleanField(default=False)),
                ('consumption', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generation_lines', to='conclusion.Consumtion')),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_powergeneration_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_powergeneration_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
