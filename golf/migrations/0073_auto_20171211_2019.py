# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-11 20:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0072_auto_20171204_0700'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournamentround',
            old_name='available_course_tees',
            new_name='course_tees',
        ),
        migrations.RenameField(
            model_name='tournamentround',
            old_name='available_courses',
            new_name='courses',
        ),
    ]
