# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0019_auto_20170809_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerplugin',
            name='name',
            field=models.CharField(blank=True, help_text='Enter the name of the plugin', max_length=200, null=True),
        ),
    ]
