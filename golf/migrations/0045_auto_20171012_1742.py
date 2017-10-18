# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0044_auto_20171011_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='net_style',
            field=models.CharField(blank=True, help_text='Enter the background-color for the cell in net view', max_length=200, null=True, verbose_name='Style Applied to the Cell for total net style'),
        ),
        migrations.AlterField(
            model_name='round',
            name='total_in_net_style',
            field=models.CharField(blank=True, help_text='Enter the background-color for the cell in net view', max_length=200, null=True, verbose_name='Style Applied to the Cell for total in net style'),
        ),
        migrations.AlterField(
            model_name='round',
            name='total_in_style',
            field=models.CharField(blank=True, help_text='Enter the background-color for the cell in gross view', max_length=200, null=True, verbose_name='Style Applied to the Cell for total in gross style'),
        ),
        migrations.AlterField(
            model_name='round',
            name='total_out_net_style',
            field=models.CharField(blank=True, help_text='Enter the background-color for the cell in net view', max_length=200, null=True, verbose_name='Style Applied to the Cell for total out net style'),
        ),
        migrations.AlterField(
            model_name='round',
            name='total_out_style',
            field=models.CharField(blank=True, help_text='Enter the background-color for the cell in gross view', max_length=200, null=True, verbose_name='Style Applied to the Cell for total out gross style'),
        ),
        migrations.AlterField(
            model_name='round',
            name='total_style',
            field=models.CharField(blank=True, help_text='Enter the background-color for the cell in gross view', max_length=200, null=True, verbose_name='Style Applied to the Cell for total gross style'),
        ),
    ]
