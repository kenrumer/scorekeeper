# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-13 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0059_auto_20171031_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='formatplugin',
            name='data',
            field=models.CharField(blank=True, help_text='Data such as username and password used to login to your clubs player data store (used by your plugin)', max_length=516, null=True),
        ),
    ]