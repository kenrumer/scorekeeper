# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 16:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0036_auto_20170914_2123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='player_type',
        ),
        migrations.AddField(
            model_name='score',
            name='round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='golf.Round', verbose_name='Round for this score'),
        ),
        migrations.DeleteModel(
            name='PlayerType',
        ),
    ]
