# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 01:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0008_coursetee_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scorecard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tee_time', models.DateField(help_text='Enter the tee time for the scorecard', verbose_name='Tee Time')),
                ('finish_time', models.DateField(help_text='Enter the finish time for the scorecard', verbose_name='Finish Time')),
                ('external_scorer', models.CharField(blank=True, help_text='Enter the name of the scorer if it is not a player', max_length=200, null=True, verbose_name='External Scorer Name')),
                ('external_attest', models.CharField(blank=True, help_text='Enter the name of the attestation if it is not a player', max_length=200, null=True, verbose_name='External Attestation Name')),
                ('attest', models.ForeignKey(blank=True, help_text='Enter the player that attests with the score', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_attest', to='golf.Player', verbose_name='Attest Player Id')),
                ('scorer', models.ForeignKey(blank=True, help_text='Enter the player that kept score', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_scorer', to='golf.Player', verbose_name='Scorer Player Id')),
            ],
        ),
        migrations.AlterField(
            model_name='coursetee',
            name='color',
            field=models.IntegerField(help_text='Enter the number associated with the tee color (0:None,1:Yellow,2:Green,3:Red,4:White,5:Blue,6:Black,7:Gold)', verbose_name='Tee Color'),
        ),
        migrations.AddField(
            model_name='round',
            name='scorecard',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='golf.Scorecard', verbose_name='Scorecard'),
            preserve_default=False,
        ),
    ]
