# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-03 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0073_auto_20171211_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerplugin',
            name='class_module',
            field=models.FileField(help_text='The class module file', null=True, upload_to='playerplugins'),
        ),
    ]
