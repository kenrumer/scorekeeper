# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-13 22:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0061_auto_20171113_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='format_data',
        ),
        migrations.AddField(
            model_name='tournamentround',
            name='format_data',
            field=models.ForeignKey(blank=True, help_text='Data required for the format plugin', null=True, on_delete=django.db.models.deletion.CASCADE, to='golf.FormatData', verbose_name='Format data'),
        ),
    ]