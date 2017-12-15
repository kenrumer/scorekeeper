# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-03 07:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0069_playerplugin_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formatplugin',
            name='filename',
        ),
        migrations.AddField(
            model_name='formatplugin',
            name='class_archive',
            field=models.FileField(help_text='The file uploaded by the user', null=True, upload_to='uploads/playerplugin'),
        ),
        migrations.AddField(
            model_name='formatplugin',
            name='class_module',
            field=models.CharField(blank=True, help_text='Enter the name of the class module', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='formatplugin',
            name='description',
            field=models.CharField(blank=True, help_text='Enter the description of the format', max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='playerplugin',
            name='description',
            field=models.CharField(blank=True, help_text='Enter the description of the format', max_length=512, null=True),
        ),
    ]
