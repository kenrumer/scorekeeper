# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-14 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0034_auto_20170913_2031'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RoundPayoutPlugin',
        ),
        migrations.RemoveField(
            model_name='format',
            name='default',
        ),
        migrations.AddField(
            model_name='format',
            name='class_name',
            field=models.CharField(blank=True, help_text='Enter the name of the class with the module', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='format',
            name='class_package',
            field=models.CharField(blank=True, help_text='Name of the module (filename with the .py) containing the class of your plugin', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='date',
            field=models.DateField(blank=True, help_text='Enter the date for the scorecard', null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='notes',
            field=models.CharField(blank=True, help_text='Enter the notes for this activity', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(blank=True, help_text='Enter the title for this activity', max_length=40, null=True),
        ),
    ]
