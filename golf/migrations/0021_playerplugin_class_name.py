# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 20:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0020_playerplugin_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerplugin',
            name='class_name',
            field=models.CharField(blank=True, help_text='Enter the name of the class with the module', max_length=200, null=True),
        ),
    ]
