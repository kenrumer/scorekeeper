# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0002_auto_20170719_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='course_tee',
            field=models.ManyToManyField(blank=True, help_text='Select the courses and tees players are playing and set the default for the card', to='golf.CourseTee', verbose_name='Course and tee'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='courses',
            field=models.ManyToManyField(blank=True, help_text='Select the courses players are playing and set the default for the card', to='golf.Course', verbose_name='Courses'),
        ),
    ]
