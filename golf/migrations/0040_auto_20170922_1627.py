# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0039_auto_20170919_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursetee',
            name='color',
            field=models.CharField(help_text='Enter the number associated with the tee color', max_length=200, verbose_name='Tee Color'),
        ),
    ]