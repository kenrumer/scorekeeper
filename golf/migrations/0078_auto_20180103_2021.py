# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-03 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0077_auto_20180103_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formatplugin',
            name='class_archive',
            field=models.FileField(help_text='The file uploaded by the user', null=True, upload_to='uploads/formatplugin'),
        ),
        migrations.AlterField(
            model_name='formatplugin',
            name='class_module',
            field=models.FileField(help_text='The class module file', null=True, upload_to='formatplugins'),
        ),
        migrations.AlterField(
            model_name='tournamentroundimportplugin',
            name='class_archive',
            field=models.FileField(help_text='The file uploaded by the user', null=True, upload_to='uploads/roundimportplugin'),
        ),
        migrations.AlterField(
            model_name='tournamentroundimportplugin',
            name='class_module',
            field=models.FileField(help_text='The class module file', null=True, upload_to='roundimportplugins'),
        ),
    ]