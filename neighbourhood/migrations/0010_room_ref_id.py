# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-11 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neighbourhood', '0009_house_ref_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='ref_id',
            field=models.CharField(default=0, max_length=32),
        ),
    ]
