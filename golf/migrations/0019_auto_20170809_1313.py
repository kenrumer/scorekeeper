# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 20:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0018_auto_20170809_1155'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerPlugin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_package', models.CharField(blank=True, help_text='Name of the module (filename with the .py) containing the class of your plugin', max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='club',
            name='club_class_name',
        ),
        migrations.RemoveField(
            model_name='club',
            name='club_class_package',
        ),
        migrations.AlterField(
            model_name='club',
            name='data',
            field=models.CharField(blank=True, help_text='Data such as username and password used to login to your clubs player data store (used by your plugin)', max_length=516, null=True),
        ),
        migrations.AddField(
            model_name='club',
            name='player_plugin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='golf.PlayerPlugin', verbose_name='Player Plugin Id'),
        ),
    ]
