# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 20:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0043_auto_20171009_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scorecard',
            name='date',
        ),
        migrations.AddField(
            model_name='scorecard',
            name='tournament_date',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='golf.TournamentDate', verbose_name='Enter the tournament date for the scorecard'),
        ),
    ]
