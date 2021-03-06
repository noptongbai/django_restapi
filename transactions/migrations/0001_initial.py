# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-02 13:43
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('units', '0001_initial'),
        ('common', '0002_auto_20170628_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdjustDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField(default=0.0)),
                ('unit_price', models.FloatField(default=0.0)),
                ('amount', models.FloatField(default=0)),
                ('humidity', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('note', models.TextField(blank=True, null=True)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_adjustdetail_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_adjustdetail_objects', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InputDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField(default=0.0)),
                ('unit_price', models.FloatField(default=0.0)),
                ('amount', models.FloatField(default=0)),
                ('humidity', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('note', models.TextField(blank=True, null=True)),
                ('truck_license', models.CharField(blank=True, max_length=255, null=True)),
                ('weighing_card', models.CharField(blank=True, max_length=255, null=True)),
                ('humidity_converted', models.FloatField(default=0)),
                ('left_quantity', models.FloatField(default=0)),
                ('used', models.BooleanField(default=False)),
                ('erp_type', models.BooleanField(default=False)),
                ('line_no', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.IntegerField(blank=True, null=True)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_inputdetail_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_inputdetail_objects', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.Supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InputJuntionAdjust',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('adjust_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjust_input_lines', to='transactions.AdjustDetail')),
                ('input_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.InputDetail')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InputJuntionReturn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('input_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.InputDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InputJuntionScrap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('input_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.InputDetail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InputJuntionWithdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('input_transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.InputDetail')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField(default=0.0)),
                ('unit_price', models.FloatField(default=0.0)),
                ('amount', models.FloatField(default=0)),
                ('humidity', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('note', models.TextField(blank=True, null=True)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_returndetail_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_returndetail_objects', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Supplier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScrapDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField(default=0.0)),
                ('unit_price', models.FloatField(default=0.0)),
                ('amount', models.FloatField(default=0)),
                ('humidity', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('note', models.TextField(blank=True, null=True)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_scrapdetail_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_scrapdetail_objects', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('types', models.IntegerField(choices=[(0, 'Input'), (1, 'Withdraw'), (2, 'Scrap'), (3, 'Return'), (4, 'Adjustment')], default=0)),
                ('note', models.TextField(blank=True, null=True)),
                ('po', models.CharField(blank=True, max_length=255, null=True)),
                ('soft_delete', models.BooleanField(default=False)),
                ('erp_type', models.BooleanField(default=False)),
                ('timestamp', models.IntegerField(blank=True, null=True)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_transaction_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_transaction_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('unit_price', models.FloatField(default=0)),
                ('quantity', models.FloatField(default=0)),
                ('synced', models.BooleanField(default=False)),
                ('adjust_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.AdjustDetail')),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_transactionlog_objects', to=settings.AUTH_USER_MODEL)),
                ('input_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.InputDetail')),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_transactionlog_objects', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('return_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.ReturnDetail')),
                ('scrap_transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.ScrapDetail')),
                ('uom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.Unit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UnitCostHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('unit_price', models.FloatField(default=0)),
                ('quantity', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField(default=0.0)),
                ('unit_price', models.FloatField(default=0.0)),
                ('amount', models.FloatField(default=0)),
                ('humidity', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('note', models.TextField(blank=True, null=True)),
                ('withdrawer_name', models.TextField(blank=True, null=True)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_withdrawdetail_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_withdrawdetail_objects', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Sector')),
                ('shift_head_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdraw_lines', to='transactions.Transaction')),
                ('uom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.Unit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='transactionlog',
            name='withdraw_transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.WithdrawDetail'),
        ),
        migrations.AddField(
            model_name='scrapdetail',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scrap_lines', to='transactions.Transaction'),
        ),
        migrations.AddField(
            model_name='scrapdetail',
            name='uom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.Unit'),
        ),
        migrations.AddField(
            model_name='returndetail',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_lines', to='transactions.Transaction'),
        ),
        migrations.AddField(
            model_name='returndetail',
            name='uom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.Unit'),
        ),
        migrations.AddField(
            model_name='inputjuntionwithdraw',
            name='withdraw_transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.WithdrawDetail'),
        ),
        migrations.AddField(
            model_name='inputjuntionscrap',
            name='scrap_transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scrap_input_lines', to='transactions.ScrapDetail'),
        ),
        migrations.AddField(
            model_name='inputjuntionscrap',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Supplier'),
        ),
        migrations.AddField(
            model_name='inputjuntionreturn',
            name='return_transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_input_lines', to='transactions.ReturnDetail'),
        ),
        migrations.AddField(
            model_name='inputjuntionreturn',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Supplier'),
        ),
        migrations.AddField(
            model_name='inputdetail',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='input_lines', to='transactions.Transaction'),
        ),
        migrations.AddField(
            model_name='inputdetail',
            name='uom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='units.Unit'),
        ),
        migrations.AddField(
            model_name='adjustdetail',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjust_lines', to='transactions.Transaction'),
        ),
        migrations.AddField(
            model_name='adjustdetail',
            name='uom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.Unit'),
        ),
    ]
