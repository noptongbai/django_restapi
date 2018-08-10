# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-16 20:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_product_product_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLedger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('entry_no', models.IntegerField()),
                ('ext_code', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.FloatField(default=0.0)),
                ('timestamp', models.IntegerField(blank=True, null=True)),
                ('created_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_productledger_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_productledger_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='created_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_product_objects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_modified_users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_product_objects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_group',
            field=models.ManyToManyField(blank=True, null=True, to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='created_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_productcategory_objects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='last_modified_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='last_modified_users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_productcategory_objects', to=settings.AUTH_USER_MODEL),
        ),
    ]