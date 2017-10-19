# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-13 00:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0045_auto_20171012_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='course_tee',
            field=models.ForeignKey(blank=True, help_text='Course and Tee This Round was Played on', null=True, on_delete=django.db.models.deletion.CASCADE, to='golf.CourseTee', verbose_name='Course and Tee'),
        ),
        migrations.AlterField(
            model_name='round',
            name='tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='golf.Tournament', verbose_name='Tournament'),
        ),
    ]