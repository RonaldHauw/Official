# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-10 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neighbourhood', '0007_auto_20161208_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='battery',
            name='charge_status',
            field=models.CharField(default=40, max_length=100),
        ),
        migrations.AddField(
            model_name='fridges',
            name='temperature',
            field=models.CharField(default=5, max_length=100),
        ),
    ]