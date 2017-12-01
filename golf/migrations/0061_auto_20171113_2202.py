# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-13 22:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0060_formatplugin_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormatData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(blank=True, help_text='Data such as username and password used to login to your clubs player data store (used by your plugin)', max_length=516, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='round',
            name='format_data',
            field=models.ForeignKey(blank=True, help_text='Data required for the format plugin', null=True, on_delete=django.db.models.deletion.CASCADE, to='golf.FormatData', verbose_name='Format data'),
        ),
    ]
