# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 00:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cardtel', '0007_auto_20170703_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='players',
        ),
        migrations.AlterField(
            model_name='player',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='cardtel.Game'),
        ),
    ]