# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 19:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0030_auto_20170824_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tee',
            name='hole',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='golf.Hole', verbose_name='Hole Id'),
        ),
    ]
