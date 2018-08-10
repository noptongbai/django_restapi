# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-02 13:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mgpAPI.validator.validate_model


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('ext_code', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.IntegerField(choices=[(0, 'Reference'), (1, 'Smaller'), (2, 'Bigger')], default=0)),
                ('ratio', models.FloatField(default=1.0, validators=[mgpAPI.validator.validate_model.validate_nonzero])),
                ('timestamp', models.IntegerField(blank=True, null=True)),
                ('soft_delete', models.BooleanField(default=False)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_unit_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_unit_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UnitCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('soft_delete', models.BooleanField(default=False)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user_unitcategory_objects', to=settings.AUTH_USER_MODEL)),
                ('last_modified_users', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_user_unitcategory_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='unit',
            name='unit_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.UnitCategory'),
        ),
    ]