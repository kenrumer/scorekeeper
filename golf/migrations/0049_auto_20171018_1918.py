# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 19:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0048_auto_20171017_1907'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TournamentPayoutPlugin',
            new_name='PayoutPlugin',
        ),
        migrations.RemoveField(
            model_name='format',
            name='plugin',
        ),
        migrations.RenameField(
            model_name='tournamentround',
            old_name='course_tees',
            new_name='available_course_tees',
        ),
        migrations.RenameField(
            model_name='tournamentround',
            old_name='courses',
            new_name='available_courses',
        ),
        migrations.RemoveField(
            model_name='round',
            name='date_finished',
        ),
        migrations.RemoveField(
            model_name='round',
            name='date_started',
        ),
        migrations.RemoveField(
            model_name='scorecard',
            name='tee_time',
        ),
        migrations.RemoveField(
            model_name='scorecard',
            name='tournament_round',
        ),
        migrations.RemoveField(
            model_name='tournamentround',
            name='date_finished',
        ),
        migrations.RemoveField(
            model_name='tournamentround',
            name='date_started',
        ),
        migrations.RemoveField(
            model_name='tournamentround',
            name='format',
        ),
        migrations.AddField(
            model_name='scorecard',
            name='start_time',
            field=models.DateTimeField(blank=True, help_text='Select the date this round was started', null=True, verbose_name='Date Started'),
        ),
        migrations.AddField(
            model_name='tournamentround',
            name='format_plugin',
            field=models.ForeignKey(blank=True, help_text='Select the scoring format for this round', null=True, on_delete=django.db.models.deletion.SET_NULL, to='golf.FormatPlugin', verbose_name='Format'),
        ),
        migrations.AlterField(
            model_name='scorecard',
            name='finish_time',
            field=models.DateTimeField(blank=True, help_text='Select the date this round was finished', null=True, verbose_name='Date Finished'),
        ),
        migrations.AlterField(
            model_name='tournamentround',
            name='name',
            field=models.CharField(help_text='Enter the name of this round of the tournament (Default is Round #)', max_length=200, verbose_name='Name'),
        ),
        migrations.DeleteModel(
            name='Format',
        ),
    ]