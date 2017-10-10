# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0042_delete_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scorecard',
            name='finish_time',
            field=models.TimeField(blank=True, help_text='Enter the finish time for the scorecard', null=True, verbose_name='Finish Time'),
        ),
        migrations.AlterField(
            model_name='scorecard',
            name='tee_time',
            field=models.TimeField(blank=True, help_text='Enter the tee time for the scorecard', null=True, verbose_name='Tee Time'),
        ),
    ]