# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 16:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neighbourhood', '0004_auto_20161205_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='ip_adress',
            new_name='ip_address',
        ),
        migrations.RenameField(
            model_name='neighbourhood',
            old_name='ip_adress',
            new_name='ip_address',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='ip_adress',
            new_name='ip_address',
        ),
    ]
