# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 19:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0053_auto_20171020_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='round',
            name='rank_net',
        ),
    ]