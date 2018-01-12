# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-24 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0056_score_skin_net'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='skin',
            field=models.IntegerField(default=False, help_text='Is this score evaluated as a skin? This changes with each scorecard submitted (1:yes, 0:no)', verbose_name='Skin'),
        ),
        migrations.AlterField(
            model_name='score',
            name='skin_net',
            field=models.IntegerField(default=False, help_text='Is this score evaluated as a skin? This changes with each scorecard submitted (1:yes, 0:no)', verbose_name='Skin'),
        ),
    ]